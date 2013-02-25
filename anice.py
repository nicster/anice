#all the imports
from __future__ import with_statement
from flask import Flask, render_template, request, flash, session, redirect, \
    url_for, jsonify, make_response
from flask.ext.assets import Environment
from PIL import Image
import os
import re
from json import JSONEncoder
from sqlite3 import dbapi2 as sqlite
from werkzeug import secure_filename
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from wtforms import Form, TextField, validators, FileField, SubmitField, HiddenField, ValidationError

#configuration
DEBUG = True
SECRET_KEY = 'anice'
USERNAME = 'admin'
PASSWORD = 'anice'
THUMBNAIL_SIZE = 128, 128
IMAGE_FOLDER = 'uploads'
THUMBNAIL_FOLDER = 'uploads/thumbnails'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
TYPE_OF_WORK = 'work'
TYPE_OF_PORTFOLIO = 'portfolio'
TYPE_OF_SKETCHES = 'sketches'
joined = '|'.join(ALLOWED_EXTENSIONS)

#create application
app = Flask(__name__)
app.config.from_object(__name__)
assets = Environment(app)


Base = declarative_base()

engine = create_engine('sqlite+pysqlite:///flaskr.db', echo=True, module=sqlite)

Session = sessionmaker(bind=engine)

ses = Session()


"""engine = create_engine('mysql+mysqldb://root:blubbi@localhost/flaskr', pool_recycle=3600)"""


@app.route('/')
def index():
    return redirect(url_for('work'))


@app.route('/portfolio')
def portfolio():
    session['type_of'] = TYPE_OF_PORTFOLIO
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('portfolio.html', site=0, form=form, paintings=paintings)


@app.route('/work')
def work():
    session['type_of'] = TYPE_OF_WORK
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('work.html', site=1, form=form, paintings=paintings)


@app.route('/sketches')
def sketches():
    session['type_of'] = TYPE_OF_SKETCHES
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('sketches.html', site=2, form=form, paintings=paintings)


@app.route('/blog')
def blog():
    form = Post_Form(request.form)
    posts = ses.query(Post).all()
    return render_template('blog.html', site=3, form=form, posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', site=4)


@app.route('/contact')
def contact():
    return render_template('contact.html', site=5)


def file_exists(filename):
    return os.path.exists("static/" + filename)


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
            response = make_response(redirect(url_for('work')))
            response.set_cookie('logged_in', True)
            return response
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    response = make_response(redirect(url_for('work')))
    response.set_cookie('logged_in', '')
    flash('You were logged out')
    return response


class Painting_Form(Form):
    title = TextField('Title', [validators.Required()])
    description = TextField('Description', [validators.Required()])
    filename = FileField('File')
    submit = SubmitField('Upload')
    hidden_id = HiddenField()

    def validate_painting(form, field):
        if field.data:
            field.data = secure_filename(re.sub(r'[^()a-z0-9_.-]', '_', str(field.data).lower()))
            field.data = session['type_of'] + field.data
            validators.regexp(r'^[^/\\]\.%s$' % joined)
            if os.path.exists(os.path.join('static/', IMAGE_FOLDER, field.data)):
                raise ValidationError('This file exists already!')


class Post_Form(Form):
    title = TextField('Title', [validators.Required()])
    text = TextField('Text', [validators.Required()])
    submit = SubmitField('Upload')
    hidden_id = HiddenField()


class Post(Base):
    __tablename__ = 'blog_entries'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    type_of = Column(String)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.type_of = session['type_of']


class Painting(Base):
    __tablename__ = 'art_gallery'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime())
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    position = Column(Integer)
    type_of = Column(String)

    def __init__(self, title, description, filename):
        self.title = title
        self.description = description
        self.filename = filename
        self.type_of = session['type_of']
        max_position = ses.query(func.max(Painting.position)).one()[0]
        if not max_position:
            max_position = 0
        print max_position
        self.position = max_position + 1

    def my_path(self):
        return os.path.join(IMAGE_FOLDER, self.filename)

    def my_thumbnail_path(self):
        return THUMBNAIL_FOLDER + '/' + self.filename

    def upload(self, file):
        print url_for('static', filename=self.my_path())
        file.save('static/' + self.my_path())
        self.create_thumbnail()

    def create_thumbnail(self):
        im = Image.open('static/' + self.my_path())
        im.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        print url_for('static', filename=self.my_thumbnail_path())
        im.save('static/' + self.my_thumbnail_path())

    def delete_uploads(self):
        os.remove('static/' + self.my_path())
        os.remove('static/' + self.my_thumbnail_path())


@app.before_request
def before_request():
    print request.base_url
    logged_in = request.cookies.get('logged_in')
    if logged_in and not session.get('logged_in'):
        session['logged_in'] = True


@app.route('/ajax/add_painting', methods=['GET', 'POST'])
def add_painting():
    form = Painting_Form(request.values)
    form.filename.process_data(request.files['filename'].filename)
    print request.script_root + '/macros.html'
    if form.validate():
        painting = Painting(form.title.data, form.description.data, form.filename.data)
        painting.upload(request.files['filename'])
        ses.add(painting)
        ses.flush()
        return jsonify(status='success', \
            content=render_template('ajax/add_painting.html', painting=painting))
    else:
        return jsonify(status='error', content=JSONEncoder().encode(form.errors)), 500


@app.route('/ajax/editing_form', methods=['GET', 'POST'])
def editing_form():
    form = Painting_Form()
    painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
    return jsonify(status='success', \
            content=render_template('ajax/editing_form.html', painting=painting, form=form))


@app.route('/ajax/edit_painting', methods=['GET', 'POST'])
def edit_painting():
    painting = ses.query(Painting).filter(Painting.id == int(request.values['hidden_id'])).one()
    form = Painting_Form(request.values, obj=painting)
    if request.files.get('filename'):
        form.filename.process_data(request.files['filename'].filename)
    else:
        form.filename.process_data(painting.filename)
    if request.method == 'POST' and form.validate():
        print form.filename.data
        form.populate_obj(painting)
        if request.files.get('filename'):
            painting.upload(request.files['filename'])
        ses.flush()
        return jsonify(status='success', \
            content=render_template('ajax/edit_painting.html', painting=painting), \
            image_id=painting.id)
    else:
        return jsonify(status='error', \
            content=form.errors), 500


@app.route('/ajax/delete_painting', methods=['POST'])
def delete_painting():
    try:
        painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
        ses.delete(painting)
        ses.flush()
        return jsonify(status='success', image_id=painting.id)
    except Exception, e:
        return jsonify(status='error', content=e), 500


@app.route('/ajax/update_paintings_order', methods=['POST'])
def update_paintings_order():
    try:
        sort_list = request.form.getlist('image[]', type=int)
        sorted_items = dict()
        counter = 1
        for item in sort_list:
            sorted_items.update({item: counter})
            counter = counter + 1
        print sorted_items
        paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).all()
        for painting in paintings:
            painting.position = sorted_items.get(painting.id)
        ses.flush()
        return jsonify(status='success')
    except Exception, e:
        raise e


@app.route('/ajax/get_description', methods=['POST'])
def get_description():
    try:
        painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
        return jsonify(
            status='success', \
            content=painting.description)
    except Exception, e:
        raise e


"""blog"""


@app.route('/ajax/add_post', methods=['GET', 'POST'])
def add_post():
    form = Post_Form(request.values)
    if form.validate():
        post = Post(form.title.data, form.text.data)
        ses.add(post)
        ses.flush()
        return jsonify(status='success', \
            content=render_template('ajax/add_post.html', post=post))
    else:
        return jsonify(status='error', content=JSONEncoder().encode(form.errors)), 500


@app.route('/ajax/editing_post_form', methods=['GET', 'POST'])
def editing_post_form():
    form = Post_Form()
    post = ses.query(Post).filter(Post.id == int(request.form['post_id'])).one()
    return jsonify(status='success', \
            content=render_template('ajax/editing_post_form.html', post=post, form=form))


@app.route('/ajax/edit_post', methods=['GET', 'POST'])
def edit_post():
    post = ses.query(Post).filter(Post.id == int(request.values['hidden_id'])).one()
    form = Post_Form(request.values, obj=post)
    if request.method == 'POST' and form.validate():
        form.populate_obj(post)
        ses.flush()
        return jsonify(status='success', \
            content=render_template('ajax/edit_post.html', post=post), \
            post_id=post.id)
    else:
        return jsonify(status='error', \
            content=form.errors), 500


@app.route('/ajax/delete_post', methods=['POST'])
def delete_post():
    try:
        post = ses.query(Post).filter(Post.id == int(request.form['post_id'])).one()
        ses.delete(post)
        ses.flush()
        return jsonify(status='success', post_id=post.id)
    except Exception, e:
        return jsonify(status='error', content=e), 500


@app.route('/submit_changes/<path:former_url>', methods=['POST', 'GET'])
def submit_changes(former_url):
    ses.commit()
    return redirect(former_url)


@app.route('/revert_changes/<path:former_url>', methods=['POST', 'GET'])
def revert_changes(former_url):
    ses.rollback()
    return redirect(former_url)


if __name__ == '__main__':
    app.run()


Base.metadata.create_all(engine)
