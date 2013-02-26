import MySQLdb

class courseDAO:
	"""
		Init course database access object
	"""
	def __init__(self):
		self.host = 'localhost'
		self.user = 'root'
		self.pwd = 'zhouyuzju'
		self.db = 'mooc'
		self.conn = MySQLdb.connect(host = self.host,user = self.user,passwd = self.pwd,db = self.db,charset='utf8')

	"""
		Insert a new record into course table
	"""
	def insert(self,record):
		cursor = self.conn.cursor()
		cursor.execute("insert into course(name,professor,university,url,detail,start_year,start_month,start_day,lasttime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
		self.conn.commit()
	
	"""
		Check if current record exists in the database
	"""
	def exist(self,url):
		cursor = self.conn.cursor()
		count = cursor.execute("select * from course where url = %s",url)
		if count == 0:
			return False
		else:
			return True
	
	"""
		Update a record if it's existing in the database
	"""
	def update(self,record):
		cursor = self.conn.cursor()
		cursor.execute("update course set name = %s,professor = %s,university = %s,url = %s,detail = %s,start_year = %s,start_month = %s,start_day = %s,lasttime = %s where url = %s",record)
		self.conn.commit()

	"""
		Close current database connection
	"""
	def __del__(self):
		self.conn.close()

if __name__ == '__main__':
	record = ['Fundamentals of Audio and Music Engineering: Part 1 Musical Sound & Electronics','Robert  Clark,Mark  Bocko','University of Rochester','https://www.coursera.org/course/audiomusicengpart1','',2013,6,3,'6']
	dao = courseDAO()
#	dao.insert(record)
	print dao.exist('https://www.coursera.org/course/audiomusicengp')
	
