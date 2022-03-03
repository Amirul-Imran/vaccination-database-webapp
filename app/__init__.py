from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")     # Set a secret key as an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vaccine.db"
db = SQLAlchemy(app)
departments = ['Mechanical', 'Electrical', 'Chemical', 'Civil', 'Biomedical']


from app import routes