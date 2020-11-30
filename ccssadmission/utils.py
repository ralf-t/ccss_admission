import sqlite3

class CurrentUser:

	username = None

	def __init__(self,username=None):
		conn = sqlite3.connect('admissions.db')
		c = conn.cursor()

		with conn:
			c.execute("delete from Session") #truncate table on every object instatiate

		self.username = username
		
		if self.username:
			self.session_login()

	def session_login(self):
		conn = sqlite3.connect('admissions.db')
		c = conn.cursor()

		with conn:
			c.execute("insert into Session (username) values (?)",(self.username,)) #insert user

	def session_logout(self):
		conn = sqlite3.connect('admissions.db')
		c = conn.cursor()

		with conn:
			c.execute("delete from Session") #truncate table

	@staticmethod
	def authenticate():
		conn = sqlite3.connect('admissions.db')
		c = conn.cursor()

		with conn:
			c.execute("select username from Session") 

		row = c.fetchone() #grab row

		if row: #if table is empty, no one is logged in
			return True
		else:
			return False

# def login()
# 	if CurrentUser.authenticate():
# 		redir to admin	
# 	redturn template

# def logout():
# 	CurrentUser.session_logout()

# def admin/applicant_edit/delete():
# 	if not CurrentUser.authenticate()
# 		redir to login
# 	return template
# 	