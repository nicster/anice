#all the imports
from flask import Flask

#configuration
DEBUG = True
SECRET_KEY = 'anice'

#create application
app = Flask(__name__)
app.config.from_object(__name__)
