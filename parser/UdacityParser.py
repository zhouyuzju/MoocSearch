from urllib2 import *
from BeautifulSoup import *

import sys
sys.path.append('../')
from dao.courseDAO import courseDAO
"""
Udacity online course web crawler(https://www.udacity.com/)
"""
class UdacityParser():

	def __init___(self):
		self.html = ''
		self.soup = None
		self.req = None

	def extract(self,url):
		self.req = urlopen(url)
		self.html = self.req.read()
		self.soup = BeautifulSoup(self.html)

	def __del__(self):
		self.req.close()

if __name__ == '__main__':
	parser = UdacityParser()
	parser.extract('https://www.udacity.com/courses')
