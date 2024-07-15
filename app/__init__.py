from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY') or "dc0d3d20a010496beddd2c1d8a0a1dba"

#app configuration
app_settings = os.environ.get(
    'APP_SETTINGS'
    'app.config'
) 
app.config.from_object(app_settings)


#connecting to database
MONGO_URI = "mongodb+srv://fabulous95:Skyview95.ii@cluster0.nz9zg.mongodb.net/E-Logbook?retryWrites=true&w=majority"

#initializing PyMongo
mongo = PyMongo(app, MONGO_URI)

from app import views
from app import admin 
