from datetime import datetime
from flask import Flask, render_template
from modules.db import initialize_app, NumberPhone

app = Flask(__name__)
initialize_app(app)


# Обработчики страниц
@app.route('/')
def index():
    count_db = NumberPhone.query.count()
    return render_template('index.html', count_db=count_db)


@app.route('/about/')
def about():
    return render_template('about.html')


# Конец обработчиков страниц


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


# Конец служебных обработчиков

if __name__ == "__main__":
    app.run(debug=True)
