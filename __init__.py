#all the imports
from __future__ import with_statement
from flask import Flask, render_template, request, flash, session, redirect, \
    url_for, jsonify, make_response, Blueprint
from PIL import Image
import os
import re
import json
import datetime
import time
from sqlite3 import dbapi2 as sqlite
from json import JSONEncoder
from werkzeug import secure_filename
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from wtforms import Form, TextField, validators, FileField, SubmitField, HiddenField, ValidationError, TextAreaField


#configuration
DEBUG = True
SECRET_KEY = 'anice'
USERNAME = 'admin'
PASSWORD = 'anice'
THUMBNAIL_SIZE = 200, 200
IMAGE_FOLDER = 'uploads'
THUMBNAIL_FOLDER = 'thumbnails'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
TYPE_OF_WORK = 'work'
TYPE_OF_PORTFOLIO = 'portfolio'
TYPE_OF_SKETCHES = 'sketches'
TYPE_OF_BLOG = 'blog'
joined = '|'.join(ALLOWED_EXTENSIONS)

#create application
app = Flask(__name__)
app.config.from_object(__name__)

instance = Blueprint("instance", __name__, static_folder=os.path.join(app.instance_path, "uploads"))
app.register_blueprint(instance)

if not os.path.exists(os.path.join(app.instance_path, 'uploads/thumbnails')) :
    os.makedirs(os.path.join(app.instance_path, 'uploads/thumbnails'), 0755)

Base = declarative_base()

"""engine = create_engine('sqlite+pysqlite:///flaskr.db', echo=True, module=sqlite)"""
engine = create_engine('mysql+mysqldb://hessiboy:Roll1679Stuhl@localhost:3306/hessiboy_anice', pool_recycle=3600)

Session = sessionmaker(bind=engine)

ses = Session()


@app.route('/')
def index():
    session['former_page'] = 'index'
    paintings = ses.query(Painting).order_by(Painting.date.desc()).all();
    if len(paintings) > 0 :
        painting = paintings[0]
    else :
        painting = None
    return render_template('home.html', site=6, painting=painting)


@app.route('/portfolio')
def portfolio():
    session['former_page'] = 'portfolio'
    session['type_of'] = TYPE_OF_PORTFOLIO
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('portfolio.html', site=0, form=form, paintings=paintings)


@app.route('/work')
def work():
    session['former_page'] = 'work'
    session['type_of'] = TYPE_OF_WORK
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('work.html', site=1, form=form, paintings=paintings)


@app.route('/sketches')
def sketches():
    session['former_page'] = 'sketches'
    session['type_of'] = TYPE_OF_SKETCHES
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('sketches.html', site=2, form=form, paintings=paintings)


@app.route('/blog')
def blog():
    """
    form = Post_Form(request.form)
    posts = ses.query(Post).all()
    return render_template('blog.html', site=3, form=form, posts=posts)
    """
    session['former_page'] = 'blog'
    session['type_of'] = TYPE_OF_BLOG
    form = Painting_Form(request.form)
    paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).order_by(Painting.position.asc()).all()
    return render_template('sketches.html', site=3, form=form, paintings=paintings)


@app.route('/about')
def about():
    session['former_page'] = 'about'
    return render_template('about.html', site=4)


@app.route('/contact')
def contact():
    session['former_page'] = 'contact'
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
            if session['former_page'] :
                response = make_response(redirect(url_for(session['former_page'])))
            else :
                response = make_response(redirect(url_for(String('work'))))
            response.set_cookie('logged_in', True)
            return response
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    if session['former_page'] :
        response = make_response(redirect(url_for(session['former_page'])))
    else :
        response = make_response(redirect(url_for(String('work'))))
    response.set_cookie('logged_in', '')
    flash('You were logged out')
    return response


class Painting_Form(Form):
    title = TextField('Title', [validators.Required()])
    description = TextAreaField('Description', [validators.Required()])
    filename = FileField('File')
    media = TextField('Media', [validators.Required()])
    submit = SubmitField('Upload')
    hidden_id = HiddenField()
    short_description = TextAreaField('Short Description', [validators.required()])

    def validate_filename(form, field):
        if field.data and not session['editing'] == 'True':
            field.data = secure_filename(re.sub(r'[^()a-z0-9_.-]', '_', str(field.data).lower()))
            field.data = session['type_of'] + field.data
            validators.regexp(r'^[^/\\]\.%s$' % joined)
            if os.path.exists(os.path.join('static/', IMAGE_FOLDER, field.data)):
                ValidationError('This file exists already!')


class Post_Form(Form):
    title = TextField('Title', [validators.Required()])
    text = TextAreaField('Text', [validators.Required()])
    submit = SubmitField('Upload')
    hidden_id = HiddenField()


class Post(Base):
    __tablename__ = 'blog_entries'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    title = Column(String(100), nullable=False)
    text = Column(String(1000), nullable=False)
    type_of = Column(String(1000))

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.type_of = session['type_of']


class Painting(Base):
    __tablename__ = 'art_gallery'

    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    filename = Column(String(100), nullable=False)
    position = Column(Integer)
    type_of = Column(String(1000))
    short_description = Column(String(1000))
    media = Column(String(100))

    def __init__(self, title, media, short_description, description, filename):
        self.title = title
        self.description = description
        self.short_description = short_description
        self.filename = filename
        self.media = media
        self.type_of = session['type_of']
        max_position = ses.query(func.max(Painting.position)).one()[0]
        if not max_position:
            max_position = 0
        print max_position
        self.position = max_position + 1
        self.date  = int(time.time());

    def my_path(self):
        return os.path.join(app.instance_path, IMAGE_FOLDER, self.filename)

    def my_thumbnail_path(self):
        return os.path.join(app.instance_path, IMAGE_FOLDER, THUMBNAIL_FOLDER, self.filename)

    def my_path_filename(self):
        return self.filename

    def my_thumbnail_path_filename(self):
        return os.path.join(THUMBNAIL_FOLDER, self.filename)

    def upload(self, file):
        file.save(self.my_path())
        self.create_thumbnail()

    def create_thumbnail(self):
        im = Image.open(self.my_path())
        height, width = im.size
        maximum = max(height, width)
        info = im.info
        if maximum > THUMBNAIL_SIZE[1]:
            im.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        im.save(self.my_thumbnail_path(), **info)

    def delete_uploads(self):
        value = 0
        try :
            os.remove(self.my_path())
        except :
            value += 1
        try : 
            os.remove(self.my_thumbnail_path())
        except :
            value += 1
        return (value == 0)


Base.metadata.create_all(engine)


@app.before_request
def before_request():
    session['editing'] = False
    logged_in = request.cookies.get('logged_in')
    if logged_in and not session.get('logged_in'):
        session['logged_in'] = True


@app.route('/ajax/add_painting', methods=['GET', 'POST'])
def add_painting():
    try:
        form = Painting_Form(request.values)
        if request.files.get('filename'):
            form.filename.process_data(request.files['filename'].filename)
        print request.script_root + '/macros.html'
        if form.validate():
            painting = Painting(form.title.data, form.media.data, form.short_description.data, form.description.data, form.filename.data)
            painting.upload(request.files['filename'])
            ses.add(painting)
            ses.flush()
            ses.commit()
            return jsonify(status='success', \
                content=render_template('ajax/add_painting.html', painting=painting))
        else:
            return jsonify(status='error', spec='form', content=json.dumps(form.errors))
    except Exception, e:
        raise e
        return jsonify(status='error', content=e.message)


@app.route('/ajax/editing_form', methods=['GET', 'POST'])
def editing_form():
    try:
        form = Painting_Form()
        painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
        return jsonify(status='success', \
                content=render_template('ajax/editing_form.html', painting=painting, form=form))
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/edit_painting', methods=['GET', 'POST'])
def edit_painting():
    try:
        session['editing'] = 'True'
        painting = ses.query(Painting).filter(Painting.id == int(request.values['hidden_id'])).one()
        form = Painting_Form(request.values, obj=painting)
        if request.files.get('filename'):
            form.filename.process_data(request.files['filename'].filename)
        else:
            form.filename.process_data(painting.filename)
        if request.method == 'POST' and form.validate():
            form.populate_obj(painting)
            if request.files.get('filename'):
                painting.upload(request.files['filename'])
            ses.flush()
            ses.commit()
            session['editing'] = 'False'
            return jsonify(status='success', \
                content=render_template('ajax/edit_painting.html', painting=painting), \
                image_id=painting.id)
        else:
            session['editing'] = 'False'
            return jsonify(status='error', spec='form', content=JSONEncoder().encode(form.errors))
    except Exception, e:
        session['editing'] = 'False'
        return jsonify(status='error', content=e.message)


@app.route('/ajax/delete_painting', methods=['POST'])
def delete_painting():
    try:
        painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
        painting.delete_uploads()
        ses.delete(painting)
        ses.flush()
        ses.commit()
        return jsonify(status='success', image_id=painting.id)
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/update_paintings_order', methods=['POST'])
def update_paintings_order():
    try:
        sort_list = request.form.getlist('image[]', type=int)
        sorted_items = dict()
        counter = 1
        for item in sort_list:
            sorted_items.update({item: counter})
            counter = counter + 1
        paintings = ses.query(Painting).filter(Painting.type_of == session['type_of']).all()
        for painting in paintings:
            painting.position = sorted_items.get(painting.id)
        ses.flush()
        ses.commit()
        return jsonify(status='success')
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/get_description', methods=['POST'])
def get_description():
    try:
        painting = ses.query(Painting).filter(Painting.id == int(request.form['image_id'])).one()
        return jsonify(
            status='success', \
            content=painting.description)
    except Exception, e:
        return jsonify(status='error', content=e.message)


"""blog"""


@app.route('/ajax/add_post', methods=['GET', 'POST'])
def add_post():
    try:
        form = Post_Form(request.values)
        if form.validate():
            post = Post(form.title.data, form.text.data)
            ses.add(post)
            ses.flush()
            ses.commit()
            return jsonify(status='success', \
                content=render_template('ajax/add_post.html', post=post))
        else:
            return jsonify(status='error', content=json.dumps(form.errors))
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/editing_post_form', methods=['GET', 'POST'])
def editing_post_form():
    try:
        form = Post_Form()
        post = ses.query(Post).filter(Post.id == int(request.form['post_id'])).one()
        return jsonify(status='success', \
            content=render_template('ajax/editing_post_form.html', post=post, form=form))
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/edit_post', methods=['GET', 'POST'])
def edit_post():
    try:
        post = ses.query(Post).filter(Post.id == int(request.values['hidden_id'])).one()
        form = Post_Form(request.values, obj=post)
        if request.method == 'POST' and form.validate():
            form.populate_obj(post)
            ses.flush()
            ses.commit()
            return jsonify(status='success',
                content=render_template('ajax/edit_post.html', post=post),
                post_id=post.id)
        else:
            return jsonify(status='error', spec='form', content=json.dumps(form.errors))
    except Exception, e:
        return jsonify(status='error', content=e.message)


@app.route('/ajax/delete_post', methods=['POST'])
def delete_post():
    try:
        post = ses.query(Post).filter(Post.id == int(request.form['post_id'])).one()
        ses.delete(post)
        ses.flush()
        ses.commit()
        return jsonify(status='success', post_id=post.id)
    except Exception, e:
        return jsonify(status='error', content=e.message)


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
