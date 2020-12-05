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
		('BSIT'),
		('BSCOMSHOP'),
		('BSHACKING'),
		('BSAI'),
		('BSML'),
		('BSDOTA')
		""")

	c.execute("""
		insert into Admin (username,password) values
		('superuser','finalsproject11111'),
		('profmoraga','finalsproject11111'),
		('ralf','finalsproject11111'),
		('jev','finalsproject11111'),
		('tiosan','finalsproject11111'),
		('anselm','finalsproject11111'),
		('renz','finalsproject11111'),
		('root','finalsproject11111'),
		('admin','finalsproject11111'),
		('sysAd','finalsproject11111')
		""")

with conn:
	c.execute("""
		insert into Applicant (lrn,first_name,last_name,shs_avg,first_course_id,second_course_id, status) values
		(22384776850,'Ryujin','Shin',99,1,NULL,'Admitted'),
		(10000000000,'Tiff','Uy',86,3,2,'Godbless'),
		(15000000000,'Phil','Health',89,4,NULL,'Godbless'),
		(85099057129,'Lightning','McQueen',95,2,6,'Godbless'),
		(40414670995,'Juan','Cruz',92,3,10,'Applied'),
		(92295973851,'Mercy','MacKenzie',88,4,NULL,'Admitted'),
		(23162636449,'Seka','Grieve',95,5,8,'Applied'),
		(46781971358,'Phillida','Overshott',91,6,NULL,'Waitlisted'),
		(44918379472,'Elane','Sprigging',81,7,10,'Admitted'),
		(27751187461,'Muffin','Greenhall',88,8,9,'Waitlisted')
		""")
