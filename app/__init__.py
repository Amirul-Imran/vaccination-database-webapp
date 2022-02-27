from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")     # Set a secret key as an environment variable
departments = ['Mechanical', 'Electrical', 'Chemical', 'Civil', 'Biomedical']

from app import routes
