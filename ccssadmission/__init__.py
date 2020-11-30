from flask import Flask

app = Flask(__name__)
app.config['SQLITE3_DATABASE_URI'] = 'admissions.db'

from ccssadmission import routes
