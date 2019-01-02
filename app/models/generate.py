from flask import Flask
from models import db
import configparser
import utils

configini = configparser.ConfigParser()
configini.read(utils.envConfigFile())


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = configini['DEFAULT']['database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()
