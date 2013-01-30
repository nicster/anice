#all the imports
from flask import Flask, render_template
from flask.ext.assets import Environment

#configuration
DEBUG = True
SECRET_KEY = 'anice'

#create application
app = Flask(__name__)
app.config.from_object(__name__)
assets = Environment(app)


@app.route('/')
def index():
    return render_template('layout.html')

if __name__ == '__main__':
    app.run()
