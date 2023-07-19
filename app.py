import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)

DB_ENGN = os.getenv('DB_ENGN')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGN}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NumberPhone(db.Model):
    __tablename__ = 'number_phone'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(14), unique=True, index=True, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
