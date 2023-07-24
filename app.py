import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory, request, send_from_directory, redirect
from sqlalchemy import desc
from modules.database import initialize_app, NumberPhone, Tag, Comment, dbase

app = Flask(__name__)
initialize_app(app)

with app.app_context():
    dbase.create_all()


# Обработчики страниц
@app.route('/')
def index():
    return render_template('index.html', count_db=NumberPhone.query.count())


@app.route('/db/')
def db():
    number_phone = NumberPhone.query.with_entities(NumberPhone.id, NumberPhone.number).order_by(
        desc(NumberPhone.id)).all()
    return render_template('db.html', all_number_db=number_phone)


@app.route('/db/<int:number>')
def more(number):
    return render_template('more.html', number=number)


@app.route('/db/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        number = request.form.get('number')
        telegram_id = request.form.get('telegram_id')
        tag = request.form.get('tag')
        comment = request.form.get('comment')

        new_number = NumberPhone(number=number, telegram_id=telegram_id)
        db.session.add(new_number)
        db.session.commit()

        new_tag = Tag(number_id=new_number.id, tag=tag)
        db.session.add(new_tag)
        db.session.commit()

        new_comment = Comment(number_id=new_number.id, comment=comment)
        db.session.add(new_comment)
        db.session.commit()

        return redirect("/")

    return render_template('add.html')


@app.route('/about/')
def about():
    return render_template('about.html')


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
    # app.run(host='192.168.1.10', port=5000, debug=True)
    app.run(debug=True)
