import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
app = Flask(__name__)
load_dotenv()
# secret key
app.secret_key = os.getenv('SECRET_KEY')

# setup password hashing
bcrypt = Bcrypt(app)

# are registrations allowed or not?
app.config['REGISTRATION_OPEN'] = os.getenv('REGISTRATION_OPEN', 'True') == 'True'

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nimbostratus.db'
db = SQLAlchemy(app)

# configure ability to update/migrate the db
migrate = Migrate(app, db)

from app import routes