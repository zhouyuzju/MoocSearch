from urllib2 import *
from BeautifulSoup import *
import datetime

import sys
sys.path.append('../')
from dao.courseDAO import courseDAO

"""
Edx online course web crawler(https://www.edx.org/courses)
"""
class EdxParser():

	"""
		Init abbreviation of university and month
	"""
	def __init__(self):
		
		self.universityDic = {'MITx':'Massachusetts Institute of Technology','HarvardX':'Harvard University','BerkeleyX':'University of California, Berkeley'}
		self.monthDic = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12,'January':1,'February':2,'March':3,'April':4,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
		self.baseUrl = 'https://www.edx.org'
		self.filterstring = '10-15 words on your course'	#annotation of course desc
		self.html = None
		self.soup = None
		self.req = None
	
	"""
		Extract info from each course
	"""
	def extract(self,url):
		self.req = urlopen(url)
		self.html = self.req.read()
		self.soup = BeautifulSoup(self.html)
		detaillist = []
		linklist = []
		namelist = []
		schoollist = []
		yearlist = []
		monthlist = []
		daylist = []
		lasttimelist = []
		instructorlist = []
		#link of each course
		for linkitem in self.soup.findAll('article',{'class':'course'}):
			url = self.baseUrl + linkitem.a['href']
			linklist.append(url)
			#open each link and get duration time of this course and the instructors
			request = urlopen(url)
			tmpHtml = request.read()
			tmpSoup = BeautifulSoup(tmpHtml)
			#when finishdate doesn't exist this section of code will throw an IndexError exception
			try:
				startdate = self.dateformat(tmpSoup.find('span',{'class':'start-date'}).contents[0])
				finishdate = self.dateformat(tmpSoup.find('span',{'class':'final-date'}).contents[0])
				lasttime = (datetime.date(finishdate[0],finishdate[1],finishdate[2]) - datetime.date(startdate[0],startdate[1],startdate[2])).days / 7	#number of weeks is the unit
				if lasttime < 0:	#something wrong in the website
					lasttime = ''
				else:
					lasttime = str(lasttime) + ' weeks'
			except:
				lasttime = ''
			lasttimelist.append(lasttime)
			instructors = ','.join([teacheritem.h3.contents[0] for teacheritem in tmpSoup.findAll('article',{'class':'teacher'})])
			instructorlist.append(instructors)
			#print instructors
			request.close()
		#extract desc of the course
		for detailitem in self.soup.findAll('div',{'class':'desc'}):
			contents = ''
			for split in detailitem.p.contents:
				if not self.filterstring in split.strip():
					contents += split.strip()
			detaillist.append(contents)
		#extract courseName of the course
		for courseNum in self.soup.findAll('span',{'class':'course-number'}):
			namelist.append(courseNum.contents[0] + courseNum.parent.contents[1])
		#extract university name of the course
		for universityitem in self.soup.findAll('a',{'class':'university'}):
			#if the name isn't in the abbreviation dic,just add the it
			if universityitem.contents[0] in self.universityDic.keys():
				schoollist.append(self.universityDic[universityitem.contents[0]])
			else:
				schoollist.append(universityitem.contents[0])
		#extract and format the start date of the course
		for dateitem in self.soup.findAll('span',{'class':'start-date'}):
			year,month,day = self.dateformat(dateitem.contents[0])
			yearlist.append(year)
			monthlist.append(month)
			daylist.append(day)
		#zip the information of the course and update the database
		for (name,url,instructor,school,detail,year,month,day,lasttime) in zip(namelist,linklist,instructorlist,schoollist,detaillist,yearlist,monthlist,daylist,lasttimelist):
			record = [name,instructor,school,url,detail,year,month,day,lasttime]
			#insert or update the database
			dao = courseDAO()
			if not dao.exist(url):
				dao.insert(record)
			else:
				record.append(url)
				dao.update(record)
			#print record
	"""
		Format the string date into (%year,%month,%day)
		Example Mar 3, 2013 ==> (2013,3,3)
	"""
	def dateformat(self,strdate):
		return int(strdate.split(',')[1].strip()),self.monthDic[strdate.split(' ')[0]],int(strdate.split(',')[0].split(' ')[1])
	
	"""
		close the opened url
	"""
	def __del__(self):
		self.req.close()
	

if __name__ == '__main__':
	edx = EdxParser()
	edx.extract('https://www.edx.org/courses')
