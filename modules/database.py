import os
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

DB_ENGN = os.getenv('DB_ENGN_DEV')
DB_USER = os.getenv('DB_USER_DEV')
DB_PASS = os.getenv('DB_PASS_DEV')
DB_HOST = os.getenv('DB_HOST_DEV')
DB_NAME = os.getenv('DB_NAME_DEV')

dbase = SQLAlchemy()


def initialize_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGN}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    dbase.init_app(app)


class NumberPhone(dbase.Model):
    tablename = 'number_phone'
    id = dbase.Column(dbase.Integer, primary_key=True)
    number = dbase.Column(dbase.String(14), unique=True, index=True, nullable=False)
    telegram_id = dbase.Column(dbase.Integer)
    registration_date = dbase.Column(dbase.DateTime, default=datetime.utcnow)


class Tag(dbase.Model):
    __tablename__ = 'tag'
    id = dbase.Column(dbase.Integer, primary_key=True)
    number_id = dbase.Column(dbase.Integer, dbase.ForeignKey('number_phone.id'), nullable=False)
    tag = dbase.Column(dbase.String(50), nullable=False)


class Comment(dbase.Model):
    __tablename__ = 'comment'
    id = dbase.Column(dbase.Integer, primary_key=True)
    number_id = dbase.Column(dbase.Integer, dbase.ForeignKey('number_phone.id'), nullable=False)
    comment = dbase.Column(dbase.Text, nullable=False)


def create_tables():
    with dbase.app.app_context():
        dbase.create_all()
