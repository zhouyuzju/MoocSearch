from urllib2 import *
from BeautifulSoup import *
import json
import datetime
import sys
sys.path.append('../')
from dao.courseDAO import courseDAO
"""
Coursera online course web crawler(https://www.coursera.org/)
"""
class CourseraParser():
	"""
		Init coursera parser
	"""
	def __init__(self):
		self.html = ''
		self.baseUrl = 'https://www.coursera.org/course/'
		self.cats = {}		#belong to which categray
		self.courses = {}	#course schedule
		self.insts = {}		#professor
		self.topics = {}	#course information
		self.unis = {}		#university

	"""
		Extract info from json response data
		Insert or update the database
	"""
	def extract(self,url):
		self.html = urlopen(url).read()		#read from json format data
		jsondata = json.loads(self.html)	#parser json data
		jsoncourses = jsondata['courses']
		jsoncats = jsondata['cats']
		jsoninsts = jsondata['insts']
		jsontopics = jsondata['topics']
		jsonunis = jsondata['unis']

		for item in jsoncats:
			self.cats[item['id']] = item
		for item in jsoncourses:
			if item['status'] == 1:		#current available courses
				self.courses[int(item['topic_id'])] = item
		for item in jsoninsts:
			self.insts[item['id']] = item
		for item in jsonunis:
			self.unis[item['id']] = item

		for id in jsontopics:
			info = jsontopics[id]
			self.topics[int(id)] = info
			university = ','.join([self.unis[unis]['name'].encode('utf-8') for unis in info.get('unis',[])])
			name = info['name'].encode('utf-8')
			url = self.baseUrl + info['short_name'].encode('utf-8')
			insts = ','.join([' '.join([self.insts[inst]['first_name'].encode('utf-8'),self.insts[inst]['last_name'].encode('utf-8')]) for inst in info.get('insts',[])])
			insts = insts.strip().strip(',')
			if not int(id) in self.courses.keys():		#courses which are not available yet
				start_year = 0
				start_month = 0
				start_day = 0
				duration_time = ''
			else:
				start_year = self.courses[int(id)]['start_year']
				start_month = self.courses[int(id)]['start_month']
				start_day = self.courses[int(id)]['start_day']
				duration_string = self.courses[int(id)]['duration_string']
				#date to be announced
				if start_year == None:start_year = 0	
				if start_month == None:start_month = 0
				if start_day == None:start_day = 0

				if duration_string == '':duration_time = 0
				else: duration_time = duration_string.split(' weeks')[0].encode('utf-8')
			detail = ''
			record = [name,insts,university,url,detail,start_year,start_month,start_day,duration_time]
			#insert or update the database
			dao = courseDAO()
			if not dao.exist(url):
				dao.insert(record)
			else:
				record.append(url)
				dao.update(record)
			#print ''.join([name,url,university,insts,str(start_year),str(start_month),str(start_day),duration_time])

if __name__ == '__main__':
	parser = CourseraParser()
	parser.extract('https://www.coursera.org/maestro/api/topic/list2?orderby=new&page=0&page-size=1000')
