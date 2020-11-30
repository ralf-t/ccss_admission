# 
# To reset db, delete admissions.db file in root directory
# then run db_setup.py again
# 
#
# To create your own querying script,
# copy paste the code below and
# write your own queries
#

# from ccssadmission import app
import sqlite3

conn = sqlite3.connect('admissions.db')

c = conn.cursor()

with conn:
	c.execute("""
		create table Course(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT UNIQUE NOT NULL
		)
		""")

	c.execute("""
		create table Admin(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL
		)
		""")

	c.execute("""
		create table Applicant(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			lrn INTEGER UNIQUE NOT NULL,
			first_name TEXT NOT NULL,
			last_name TEXT NOT NULL,
			shs_avg INT NOT NULL,
			status TEXT NOT NULL DEFAULT 'Applied',
			first_course_id INTEGER NOT NULL,
			second_course_id INTEGER,

			FOREIGN KEY(first_course_id) REFERENCES Course(id),
			FOREIGN KEY(second_course_id) REFERENCES Course(id)
		)
		""")

	c.execute("""
		create table Session(
			id INTEGER PRIMARY KEY CHECK (id = 1),
			username TEXT UNIQUE NOT NULL
		)
		""")

	c.execute("""
		insert into Course (name) values
		('BSCS'),
		('BSEMC-DA'),
		('BSEMC-GD'),
		('BSIS'),
		('BSIT')
		""")

	c.execute("""
		insert into Admin (username,password) values
		('superuser','finalsproject11111'),
		('profmoraga','finalsproject11111')
		""")

with conn:
	c.execute("""
		insert into Applicant (lrn,first_name,last_name,shs_avg,first_course_id,second_course_id) values
		(22384776850,'Ryujin','Shin',99,1,NULL),
		(10000000000,'Tiff','Uy',86,3,2),
		(15000000000,'Phil','Health',89,4,NULL),
		(85099057129,'Lightning','McQueen',95,5,3),
		(40414670995,'Juan','Cruz',92,2,4)
		""")

