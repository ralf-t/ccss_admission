from flask import Flask
import sqlite3

app = Flask(__name__)
# app.config['SQLITE3_DATABASE_URI'] = 'sqlite:///blogs.db'

current_user = None #store entire row

from ccssadmission import routes