from flask import render_template, url_for, redirect, request, abort
from ccssadmission import app
from ccssadmission.utils import CurrentUser
import sqlite3

current_user = CurrentUser()

@app.route("/",methods=["GET","POST"])
@app.route("/apply",methods=["GET","POST"])
def apply():
	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI']) #creating the connecting object
	c = conn.cursor() #setting cursor

	errors = []
	success = None

	if request.method == 'POST':
		lrn = request.form['lrn']
		lastName = request.form['lastName']
		first_name = request.form['firstName']
		shs_avg = request.form['avgGrade']
		first_course_id = request.form['priorityChoice']
		second_course_id = request.form['secondChoice'] if request.form['secondChoice'] != 'empty' else None

		#check duplicate lrn
		with conn:	
			c.execute("pragma foreign_keys=ON") #important to enforce FK constraints
			
			c.execute("select * from Applicant where lrn=?", (lrn,))
			if c.fetchone(): #if there is existing student with same LRN, return error
				errors.append('LRN is registered by another applicant')

			if not errors: #if LRN is unique, save data into db
				c.execute("INSERT INTO Applicant (lrn, first_name, last_name, shs_avg, first_course_id, second_course_id)VALUES (?, ?, ?, ?, ?, ?)", (lrn, first_name, lastName, shs_avg, first_course_id, second_course_id))
				success = ("Congratulations! You have successfully been applied.")

	return render_template('apply.html', errors=errors, success=success)

@app.route("/results",methods=["GET","POST"])
def results():

	return render_template('results.html')

@app.route("/results/<int:lrn>")
def results_lrn(lrn):
	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
	c = conn.cursor()

	with conn:
		c.execute("SELECT * FROM Applicant WHERE lrn=?",(lrn,))
		applicant = c.fetchone()

		c.execute("SELECT * FROM Course WHERE Course.id=(SELECT first_course_id FROM Applicant WHERE lrn=?)",(lrn,))
		course1 = c.fetchone()

		c.execute("Select * FROM Course WHERE Course.id=(SELECT second_course_id FROM Applicant WHERE lrn=?)",(lrn,))
		course2 = c.fetchone()
		
	#first_or_404 check
	return render_template('results_lrn.html', applicant=applicant, course1=course1, course2=course2)

@app.route("/login",methods=["GET","POST"])
def login():

	global current_user
	if CurrentUser.authenticate():
		return redirect(url_for('admin'))

	errors = []
	error = request.args.get('error')

	if request.args.get('error'):
		errors.append(error)

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
		c = conn.cursor() 
		with conn:
			c.execute("select username, password from Admin where username=? and password=?",(username,password))
			user = c.fetchone()

		if user:
			global current_user
			current_user = CurrentUser(user[0])
			return redirect(url_for('admin',success=f'Welcome {user[0]} to the admin dashboard!'))
		else:
			errors = ['Invalid username or password']
	return render_template('login.html',errors=errors)

@app.route("/logout")
def logout():	
	current_user.session_logout()
	return redirect(url_for('login'))

@app.route("/admin",methods=["GET","POST"])
def admin():

	global current_user
	if not CurrentUser.authenticate():
		return redirect(url_for('login',error='Admin login required'))

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
	c = conn.cursor()
	if request.method == 'POST':
		lrn = request.form['lrn']
		with conn:
			c.execute("""select a.id, a.lrn, a.first_name, a.last_name, a.shs_avg, a.status, f.name, s.name
								from Applicant a 
								left join course f
								on f.id = a.first_course_id
								left join course s
								on s.id = a.second_course_id
								where a.lrn=?""",(lrn,))
			rows = c.fetchall()
			return render_template('admin.html', rows=rows)		
	else:	
		with conn:
			c.execute("""select a.id, a.lrn, a.first_name, a.last_name, a.shs_avg, a.status, f.name, s.name
						from Applicant a 
						left join course f
						on f.id = a.first_course_id
						left join course s
						on s.id = a.second_course_id""")
			rows = c.fetchall()
			return render_template('admin.html', rows=rows,success=request.args.get('success'))

@app.route("/admin/applicant/edit/<int:applicant_id>",methods=["GET","POST"])
def applicant_edit(applicant_id):
	# <int:applicant_id> means we are getting a string value in our url and casting it to int

	global current_user
	if not CurrentUser.authenticate():
		return redirect(url_for('login'))

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI']) #creating the connecting object
	c = conn.cursor() #setting cursor

	query = None #variable to hold our result
	courses = None
	
	errors = []
	success = None

	if request.method == 'POST':
		lrn = request.form['lrn']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		shs_avg = request.form['shs_avg']
		status = request.form['status']
		first_course_id = request.form['first_course_id']
		second_course_id = request.form['second_course_id'] if request.form['second_course_id'] != 'Select course' else None

		#check duplicate lrn
		with conn:	
			c.execute("pragma foreign_keys=ON") #important to enforce FK constraints
			c.execute("select * from Applicant where lrn=? and id !=? ",(lrn,applicant_id,))
			
			if c.fetchall():
				errors.append('LRN is registered by another applicant')

			if not errors:
				c.execute("""
					update Applicant
					set lrn=?, first_name=?, last_name=?, shs_avg=?, status=?, first_course_id=?, second_course_id=?
					where id=?
					""",(lrn,first_name,last_name,shs_avg,status,first_course_id,second_course_id,applicant_id,))

				success = f"Details updated for applicant {applicant_id}"

	with conn:	# to safely interact with our resource and avoids the burden of manually closing resources.
		c.execute("select * from Applicant where id=?",(applicant_id,)) #use ? for safe db transaction. applicant_id variable is taken from url parameters
		query = c.fetchone() #fetchone to a tuple of result. fetchall to get a tuple list of results
		c.execute("select * from Course")
		courses = c.fetchall()

	#pag walang result si c.fetchone(), None ang narereturn
	#passing our query variable to another variable named query in the return statement
	#passing din ng errors. see base.html to know how errors are displayed
	#python handles variable scopes in a different way
	if query: 
		return render_template('applicant_edit.html',query=query,courses=courses,errors=errors,success=success) 
	else:
		return abort(404)

@app.route("/admin/applicant/delete/<int:applicant_id>",methods=["POST"])
def applicant_delete(applicant_id):

	global current_user
	if not CurrentUser.authenticate():
		return redirect(url_for('login'))


	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI']) 
	c = conn.cursor() 

	query = None 
	courses = None
	
	errors = []
	success = None

	if request.method == 'POST':
		lrn = request.form['lrn']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		shs_avg = request.form['shs_avg']
		status = request.form['status']
		first_course_id = request.form['first_course_id']
		second_course_id = request.form['second_course_id'] if request.form['second_course_id'] != 'Select course' else None

		with conn:	
			c.execute("pragma foreign_keys=ON") 
			c.execute("select * from Applicant where lrn=? and id=? ",(lrn,applicant_id,))
			
			c.execute("""DELETE from Applicant where lrn=?, first_name=?, last_name=?, shs_avg=?, status=?, 
				first_course_id=?, second_course_id=?, id=?""",(lrn,first_name,last_name,shs_avg,status,first_course_id,second_course_id,applicant_id,))
			success = f"Details delete for applicant {applicant_id}"

	if query: 
		return redirect(url_for('admin'),query=query,courses=courses,errors=errors,success=success) 
