from flask import render_template, url_for, redirect, request
from ccssadmission import app, current_user

@app.route("/")
@app.route("/apply")
def apply():
	#edit
	return render_template('apply.html')

@app.route("/results")
def results():
	#edit
	return render_template('results.html')

@app.route("/results/lrn")
def results_lrn():
	#edit
	return render_template('results_lrn.html')

@app.route("/login")
def login():
	#edit
	return render_template('login.html')

@app.route("/admin")
def admin():
	#edit
	return render_template('admin.html')

@app.route("/admin/applicant/id")
def applicant():
	#edit
	return render_template('applicant.html')

@app.route("/admin/applicant/id")
def applicant_edit():
	#edit
	return render_template('applicant_edit.html')
