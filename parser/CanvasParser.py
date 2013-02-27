from urllib2 import *
from BeautifulSoup import *

import sys
sys.path.append('../')
from dao.courseDAO import courseDAO
"""
Canvas.net online course web crawler(https://www.canvas.net/)
"""
class CanvasParser():
	"""
		Init the dic
	"""
	def __init__(self):
		self.html = ''
		self.soup = None
		#abbreviation to digital dic
		self.MONTHDIC = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}	
	"""
		Extract course info by BeautifulSoup.
		Won't work when web document changes
	"""
	def extract(self,url):
		self.html = urlopen(url).read()
		self.soup = BeautifulSoup(self.html)
		courseLinks = self.soup.findAll('a',{'class':'featured-course-live'})
		courseNames = self.soup.findAll('span',{'class':'featured-course-title'})
		schoolNames = self.soup.findAll('div',{'class':'featured-course-school'})
		instructorNames = self.soup.findAll('h5',{'class':'last emboss-light instructor-name'})
		courseDetails = self.soup.findAll('p',{'class':'last fineprint pad-box-mini top-rule-box featured-course-desc'})

		for (itemname,iteminstructor,itemschool,itemlink,itemdetail) in zip(courseNames,instructorNames,schoolNames,courseLinks,courseDetails):
			detail = itemdetail.contents[0].encode('utf-8')
			instructor = iteminstructor.contents[0].split(',')[0]
			school = itemschool.div.img['title']
			name = itemname.span.contents[0]
			url = itemlink['href']
			date = itemlink.span.contents[2]	#format like:\blank Feb 25,\blank 2012\n\blank
			year = int(date.strip().split(',')[1])
			month = self.MONTHDIC[date.strip().split()[0]]
			day = int(date.strip().split(',')[0].split()[1])
			lasttime = ''
			record = [name,instructor,school,url,detail,year,month,day,lasttime]
			#insert or update the database
			dao = courseDAO()
			if not dao.exist(url):
				dao.insert(record)
			else:
				record.append(url)
				dao.update(record)

if __name__ == '__main__':
	parser = CanvasParser()
	parser.extract('https://www.canvas.net/')
