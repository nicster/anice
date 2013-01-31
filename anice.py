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

<<<<<<< HEAD

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

=======
>>>>>>> 5ce2fe2eb53f54476459ff7374d4a85664804f25
if __name__ == '__main__':
    app.run()
