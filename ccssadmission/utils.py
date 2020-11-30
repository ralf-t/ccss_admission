import sqlite3

class CurrentUser:
	self.username = None
	self.db_uri = ['admissions.db']
	self.conn = sqlite3.connect(self.db_uri)
	self.c = self.conn.cursor()

	def init(self,username=None):
		with self.conn:
			self.c.execute("delete from Session") #truncate table on every object instatiate

		self.username = username
		
		if self.username:
			self.session_login()

	def session_login(self):
		with self.conn:
			self.c.execute("insert into Session (username) values (?)",(self.username,)) #insert user

	def session_logout(self):
		with self.conn:
			self.c.execute("delete from Session") #truncate table

	@staticmethod
	def authenticate():
		with self.conn:
			self.c.execute("select username from Session where username = ?") 

		rows = self.c.fetchall() #grab rows

		if len(rows) == 1: #if table is empty, no one is logged in

			row = rows[0] #username index

			if row[0] == self.username: #check if 
				return True
			else:
				return False 
		else:
			return False

