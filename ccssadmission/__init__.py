from flask import Flask
from ccssadmission.utils import CurrentUser

app = Flask(__name__)
app.config['SQLITE3_DATABASE_URI'] = 'admissions.db'

current_user = CurrentUser() #store entire row

from ccssadmission import routes