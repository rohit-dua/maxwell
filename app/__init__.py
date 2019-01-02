from flask import Flask, request
import os
from flask_migrate import Migrate
import configparser


app = Flask(__name__)
app.globalPath = os.path.abspath(os.path.dirname(__file__))

import utils
configini = configparser.ConfigParser()
configini.read(utils.envConfigFile())
app.configini = configini

app.config['SQLALCHEMY_DATABASE_URI'] = configini['DEFAULT']['database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import routes
from models import db
db.init_app(app)
