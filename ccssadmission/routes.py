from flask import render_template, url_for, redirect, request, abort
from ccssadmission import app, current_user
from ccssadmission.utils import authenticate, login, logout
import sqlite3

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

@app.route("/results/lrn")
def results_lrn():
	#edit
	return render_template('results_lrn.html')

@app.route("/login",methods=["GET","POST"])
def login():
	errors = []
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI'])
		c = conn.cursor() 
		with conn:
			c.execute("select username, password from Admin where username=? and password=?",(username,password))
			user = c.fetchone()

		if user:
			return redirect("/admin")
		else:
			errors = ['Invalid username or password']
	return render_template('login.html',errors=errors)

@app.route("/admin")
def admin():
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
			return render_template('admin.html', rows=rows)

@app.route("/admin/applicant/edit/<int:applicant_id>",methods=["GET","POST"])
def applicant_edit(applicant_id):
	# <int:applicant_id> means we are getting a string value in our url and casting it to int
	
	global current_user

	current_user = authenticate(request.args.get('admin')) if request.args.get('admin') else False
	
	if not current_user:
		return redirect(url_for('login',login_error="Please login to access admin dashboard"))
	

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
		return render_template('applicant_edit.html',query=query,courses=courses,errors=errors,success=success,admin=current_user[3]) 
	else:
		return abort(404)

@app.route("/admin/applicant/delete/<int:applicant_id>",methods=["POST"])
def applicant_delete(applicant_id):
	return redirect(url_for('admin'))

