from urllib2 import *
from BeautifulSoup import *

import sys
sys.path.append('../')
from dao.courseDAO import courseDAO
"""
Udacity online course web crawler(https://www.udacity.com/)
"""
class UdacityParser():
	"""
		Init base url and schoolName.
		All the courses' school name are equal to udacity
	"""
	def __init__(self):
		self.html = ''
		self.soup = None
		self.req = None
		self.baseUrl = 'https://www.udacity.com'
		self.schoolName = 'udacity'	
		self.url = []
		self.courseName = []
		self.instructor = []
		self.detail = []

	"""
		Extract info from udacity
	"""
	def extract(self,url):
		self.req = urlopen(url)
		self.html = self.req.read()
		self.soup = BeautifulSoup(self.html)
		#url list
		courselist = self.soup.find('ul',id = 'unfiltered-class-list')	
		
		"""
			get a list of urls of all the courses here.
			parser each url and may throw exceptions here.
			Todo:exceptions handling
		"""
		for linkitem in courselist.findAll('a'):
			#get the course url
			url = self.baseUrl + linkitem['href']
			#parser the course index page
			self.url.append(url)
			#print url
			request = urlopen(url)
			tmpHtml = request.read()
			tmpSoup = BeautifulSoup(tmpHtml)
			#get detail and instructors information
			detail = tmpSoup.find('div',{'class':'span3'}).findAll('p')[1].contents[0]
			instructors = ','.join([item.contents[0].encode('utf-8') for item in tmpSoup.findAll('span',{'class':'oview-side-instr'})])
			self.instructor.append(instructors)
			self.detail.append(detail)
			request.close()

		for titleitem,subitem in zip(courselist.findAll('div',{'class':'crs-li-title'}),courselist.findAll('div',{'class':'crs-li-sub'})):
			#get course name and subname
			name = titleitem.contents[0].strip() + '-' + subitem.contents[0].strip()
			self.courseName.append(name)
		
		for (name,url,instructor,detail) in zip(self.courseName,self.url,self.instructor,self.detail):
			start_year = 0
			start_month = 0
			start_day = 0
			lasttime = ''
			record = [name,instructor,self.schoolName,url,detail,start_year,start_month,start_day,lasttime]
			#insert or update the database
			dao = courseDAO()
			if not dao.exist(url):
				dao.insert(record)
			else:
				record.append(url)
				dao.update(record)	
			#print record

	def __del__(self):
		self.req.close()

if __name__ == '__main__':
	parser = UdacityParser()
	parser.extract('https://www.udacity.com/courses')
