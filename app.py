import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory
from sqlalchemy import desc
from modules.db import initialize_app, NumberPhone, db

app = Flask(__name__)
initialize_app(app)

with app.app_context():
    db.create_all()


# Обработчики страниц
@app.route('/')
def index():
    return render_template('index.html', count_db=NumberPhone.query.count())


@app.route('/db/')
def db():
    number_phone = NumberPhone.query.with_entities(NumberPhone.id, NumberPhone.number).order_by(
        desc(NumberPhone.id)).all()

    return render_template('db.html', all_number_db=number_phone)


@app.route('/db/<number>')
def more(number):
    return render_template('more.html', number=number)


@app.route('/db/add/')
def add(number):
    return render_template('add.html', number=number)


# Конец обработчиков страниц

# --------------------------

# Служебные обработчики
@app.errorhandler(404)
def handle_bad_request_404(e):
    return render_template('404.html'), 404


@app.errorhandler(503)
def handle_bad_request_503(e):
    return render_template('503.html'), 503


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Конец служебных обработчиков

if __name__ == "__main__":
    app.run(host='192.168.1.10', port=5000, debug=True)
