from flask import render_template, url_for, redirect, request
from ccssadmission import app, current_user

@app.route("/")
@app.route("/apply")
def apply():
	return render_template('apply.html')

@app.route("/results")
def results():
	return render_template('results.html')

@app.route("/results/lrn")
def results_lrn():
	return render_template('results_lrn.html')

@app.route("/login")
def login():
	#editorssss
	#editorssss
	#editorssss
	#editorssss
	#editorssss
	#editorssss

	return render_template('login.html')

@app.route("/admin")
def admin():
	#editorssss
	#editorssss
	#editorssss
	#editorssss
	#editorssss
	#editorssss

	return render_template('admin.html')

@app.route("/admin/applicant/id")
def applicant():
	#editorssss
	return render_template('applicant.html')

@app.route("/admin/applicant/id")
def applicant_edit():
	return render_template('applicant_edit.html')
