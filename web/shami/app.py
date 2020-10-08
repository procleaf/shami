#! /usr/bin/env python3

import os

from flask import Flask, render_template, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
import werkzeug.exceptions as ex

import click

from forms import LoginForm

from shami.utils import list_file

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')

prefix = 'sqlite:////'
app.config['LOG_DB_FILE'] = os.path.join(os.getenv('SHAMI'), 'log.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + app.config['LOG_DB_FILE'])
app.config['SHAMI_ROOT_DIR'] = os.getenv('SHAMI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class PathDoesNotExist(ex.HTTPException):
    code = 404
    description = "<p>Path does not exist.</p>"

class ShamiLog(db.Model):
    __tablename__ = "shamilog"
    id = db.Column(db.Integer, primary_key=True)
    tester = db.Column(db.String(20))
    feature = db.Column(db.String(20))
    version = db.Column(db.String(20))
    logurl = db.Column(db.String(50))

@app.errorhandler(404)
def no_such_path(e):
    return "Path does not exist."

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Database initialized.")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash(f"Welcome, {username}")
    return render_template('login.html', form=form)

@app.route('/logs')
def logs():
    shamilogs = ShamiLog.query.all()
    return render_template('logs.html', shamilogs=shamilogs)

@app.route('/tasks')
def tasks():
    """List tasks"""
    tasks_path = os.path.join(app.config['SHAMI_ROOT_DIR'], "tasks")
    if not os.path.isdir(tasks_path):
        abort(404)
    tasks_files = []
    for t in list_file(tasks_path):
        tasks_files.append(os.path.basename(t))
    return render_template('tasks.html', tasks_files=tasks_files)

@app.route('/submit-task', methods=['GET', 'POST'])
def submit_task():
    return render_template('submit_task.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register for an account."""
    return render_template('register.html')

@app.route('/task-overview', methods=['GET', 'POST'])
def task_overview():
    return 'This is the task overview page.'

@app.route('/resources')
def resources():
    """The resource page"""
    resouces_path = os.path.join(app.config['SHAMI_ROOT_DIR'], 'resources')
    if not os.path.isdir(resouces_path):
        abort(404)
    res = []
    for r in list_file(resouces_path):
        _r = {
                "abspath": r,
                "path": os.path.basename(r).strip('.lck'),
                # "pc1.lck" means resource is locked by the system.
                "locked": True if r.endswith('.lck') else False
             }

        res.append(_r)
    return render_template('resources.html', res=res)

@app.cli.command()
@click.option('--count', default=20, help='Quantity of fake data')
def create_fake_data(count):
    """Create fake data"""
    from faker import Faker
    
    fake = Faker()

    click.echo("Generating fake data...")

    for i in range(count):
        log = ShamiLog(tester=fake.name(),
                version=fake.random_int(),
                feature=fake.word(),
                logurl=fake.image_url()
                )
        db.session.add(log)
    db.session.commit()
    click.echo(f"Generated {count} fake data.")
