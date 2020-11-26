from flask import Flask

app = Flask(__name__)
app.config['SQLITE3_DATABASE_URI'] = 'admissions.db'

current_user = None #store entire row

from ccssadmission import routes