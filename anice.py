#all the imports
from flask import Flask, render_template, request, flash, session, redirect, \
url_for
from flask.ext.assets import Environment

#configuration
DEBUG = True
SECRET_KEY = 'anice'
USERNAME = 'admin'
PASSWORD = 'anice'

#create application
app = Flask(__name__)
app.config.from_object(__name__)
assets = Environment(app)


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', site=0)


@app.route('/work')
def work():
    return render_template('work.html', site=1)


@app.route('/sketches')
def sketches():
    return render_template('sketches.html', site=2)


@app.route('/blog')
def blog():
    return render_template('blog.html', site=3)


@app.route('/about')
def about():
    return render_template('about.html', site=4)


@app.route('/contact')
def contact():
    return render_template('contact.html', site=5)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You successfully logged in')
            return redirect(url_for('work'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()
