import os
from datetime import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for

load_dotenv()

app = Flask(__name__)

DB_ENGN = os.getenv('DB_ENGN_DEV')
DB_USER = os.getenv('DB_USER_DEV')
DB_PASS = os.getenv('DB_PASS_DEV')
DB_HOST = os.getenv('DB_HOST_DEV')
DB_NAME = os.getenv('DB_NAME_DEV')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGN}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NumberPhone(db.Model):
    __tablename__ = 'number_phone'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(14), unique=True, index=True, nullable=False)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/')
def index():
    count_db = NumberPhone.query.count()
    return render_template('index.html', count_db=count_db)


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
