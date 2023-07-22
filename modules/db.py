import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

DB_ENGN = os.getenv('DB_ENGN_DEV')
DB_USER = os.getenv('DB_USER_DEV')
DB_PASS = os.getenv('DB_PASS_DEV')
DB_HOST = os.getenv('DB_HOST_DEV')
DB_NAME = os.getenv('DB_NAME_DEV')

db = SQLAlchemy()


def initialize_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGN}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


class NumberPhone(db.Model):
    tablename = 'number_phone'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(14), unique=True, index=True, nullable=False)


def create_tables():
    with db.app.app_context():
        db.create_all()
