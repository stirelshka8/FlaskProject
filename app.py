import os
import logging
from sqlalchemy import desc
from datetime import datetime
from modules.database import initialize_app, NumberPhone, Tag, Comment, dbase
from flask import Flask, render_template, request, send_from_directory, redirect

logging.basicConfig(level=logging.INFO, filename="flask_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)
initialize_app(app)

try:
    with app.app_context():
        dbase.create_all()
except Exception as ex:
    logging.error(ex)


# Обработчики страниц
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'GET':
            count_db = NumberPhone.query.count()
            return render_template('index.html', count_db=count_db)
        elif request.method == 'POST':
            selected_name = request.form.get('number')
            search_phone_number = NumberPhone.query.filter_by(number=selected_name).first()

            if search_phone_number is None:
                return render_template('not_number.html')
            else:
                return redirect(f"/db/{search_phone_number.id}")
    except Exception as exc:
        logging.error(exc)
        return render_template('index.html', count_db="...")


@app.route('/db/')
def db():
    # добавляем пагинацию
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    # получаем список номеров телефонов с использованием пагинации
    try:
        number_phone = NumberPhone.query.with_entities(NumberPhone.id, NumberPhone.number, Tag.tag).order_by(
            desc(NumberPhone.id)).join(Tag).paginate(page=page, per_page=per_page)

        return render_template('db.html', all_number_db=number_phone)
    except Exception as exc:
        logging.error(exc)
        return render_template('503.html'), 503


@app.route('/db/<int:number>', methods=['GET', 'POST'])
def more(number):
    number_phone_entry = NumberPhone.query.filter_by(id=number).first()
    tags_entries = Tag.query.filter_by(number_id=number).all()

    page = request.args.get('page', 1, type=int)
    per_page = 5
    comments_entries = Comment.query.filter_by(number_id=number).order_by(Comment.id.desc()) \
        .paginate(page=page, per_page=per_page)

    if request.method == 'POST':
        selected_name = request.form.get('name')
        selected_comment = request.form.get('comment')

        new_comment = Comment(number_id=number, name=selected_name, comment=selected_comment)
        dbase.session.add(new_comment)
        dbase.session.commit()

        return redirect(request.url)

    return render_template('more.html', number=number_phone_entry, tags=tags_entries, comments=comments_entries)


@app.route('/db/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        selected_country = request.form.get('country')
        number = request.form.get('number')
        telegram_id = request.form.get('telegram_id')
        name = request.form.get('user_name')
        email = request.form.get('user_email')
        tag = request.form.get('tag')

        format_number = f"{selected_country}{number}"

        try:
            new_number = NumberPhone(number=format_number, telegram_id=telegram_id, name=name, email=email)
            dbase.session.add(new_number)
            dbase.session.commit()

            new_tag = Tag(number_id=new_number.id, tag=tag)
            dbase.session.add(new_tag)
            dbase.session.commit()

        except Exception as exc:
            logging.error(exc)
            return render_template('503.html'), 503

        return redirect("/db/")

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
    app.run(host='192.168.1.10', port=5000, debug=True)
    # app.run(debug=True)
