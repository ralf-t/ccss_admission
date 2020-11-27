from ccssadmission import app
import sqlite3


def authenticate(admin_id):

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
	c = conn.cursor() 

	with conn:
		
		c.execute("select * from Admin where id=?",(admin_id,))
		admin = c.fetchone()

		if admin and admin[3] != 0: #if user exists and is is logged in
			current_user=admin
			return current_user
		
		else: 
			return False

def login(admin_id):

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
	c = conn.cursor() 

	with conn:
		c.execute("select * from Admin where id=?",(admin_id,))

		if c.fetchone(): #if user exists, set login status to 1 
			c.execute("""
				update Admin
				set login_status=1
				where id=?
				""",(admin_id,))
			
			current_user=c.fetchone()
			return current_user
			
		else: 
			return False

def logout(admin_id):

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
	c = conn.cursor() 

	with conn:
		c.execute("select * from Admin where id=?",(admin_id,))

		if c.fetchone(): #if user exists, login status to 0 then redirect to login page
			c.execute("""
				update Admin
				set login_status=0
				where id=?
				""",(admin_id,))
			
			current_user = None
			return current_user

		else: 
			return False
