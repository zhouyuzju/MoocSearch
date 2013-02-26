import MySQLdb

class courseDAO:

	def __init__(self):
		self.host = 'localhost'
		self.user = 'root'
		self.pwd = 'zhouyuzju'
		self.db = 'mooc'
		self.conn = MySQLdb.connect(host = self.host,user = self.user,passwd = self.pwd,db = self.db,charset='utf8')

	def insert(self,record):
		cursor = self.conn.cursor()
		cursor.execute("insert into course(name,professor,university,url,detail,start_year,start_month,start_day,lasttime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",record)
		self.conn.commit()

	def select(self):
		cursor = self.conn.cursor()
		count = cursor.execute("select * from course")
		print count
	
	def __del__(self):
		self.conn.close()

if __name__ == '__main__':
	record = ['Fundamentals of Audio and Music Engineering: Part 1 Musical Sound & Electronics','Robert  Clark,Mark  Bocko','University of Rochester','https://www.coursera.org/course/audiomusicengpart1','',2013,6,3,'6']
	dao = courseDAO()
#	dao.insert(record)
	dao.select()
	
