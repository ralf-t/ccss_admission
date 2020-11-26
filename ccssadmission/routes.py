from flask import render_template, url_for, redirect, request, abort
from ccssadmission import app, current_user
import sqlite3

@app.route("/",methods=["GET","POST"])
@app.route("/apply",methods=["GET","POST"])
def apply():
	#edit
	return render_template('apply.html')

@app.route("/results",methods=["GET","POST"])
def results():

	return render_template('results.html')

@app.route("/results/lrn")
def results_lrn():
	#edit
	return render_template('results_lrn.html')

@app.route("/login",methods=["GET","POST"])
def login():
	#edit
	return render_template('login.html')

@app.route("/admin")
def admin():
	#edit
	return render_template('admin.html')

@app.route("/admin/applicant/edit/<int:applicant_id>",methods=["GET","POST"])
def applicant_edit(applicant_id):
	# <int:applicant_id> means we are getting a string value in our url and casting it to int

	conn = sqlite3.connect(app.config['SQLITE3_DATABASE_URI']) #creating the connecting object
	c = conn.cursor() #setting cursor

	query = None #variable to hold our result
	courses = None

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
		return render_template('applicant_edit.html',query=query,courses=courses,errors=['Passing errors variable']) 
	else:
		return abort(404)
