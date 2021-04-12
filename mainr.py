from flask import Flask, request, render_template, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
import flask

import datetime
from data import db_session
from data.users import User
from data.login_form import LoginForm
from data.register import RegisterForm

photos = ['main/0.jpg', 'main/1.jpg', 'main/2.jpg', 'main/3.jpg', 'main/4.jpg', 'main/5.jpg']

scetch = ['scetchbook/(1).jpg', 'scetchbook/(2).jpg', 'scetchbook/(3).jpg', 'scetchbook/(4).jpg',
          'scetchbook/(5).jpg', 'scetchbook/(6).jpg', 'scetchbook/(7).jpg', 'scetchbook/(8).jpg',
          'scetchbook/(9).jpg', 'scetchbook/(10).jpg', 'scetchbook/(11).jpg', 'scetchbook/(12).jpg',
          'scetchbook/(13).jpg', 'scetchbook/(14).jpg', 'scetchbook/(15).jpg', 'scetchbook/(16).jpg',
          'scetchbook/(17).jpg', 'scetchbook/(18).jpg', 'scetchbook/(19).jpg', 'scetchbook/(20).jpg',
          'scetchbook/(21).jpg', 'scetchbook/(22).jpg', 'scetchbook/(23).jpg', 'scetchbook/(24).jpg',
          'scetchbook/(25).jpg', 'scetchbook/(26).jpg', 'scetchbook/(27).jpg', 'scetchbook/(28).jpg',
          'scetchbook/(29).jpg', 'scetchbook/(30).jpg', 'scetchbook/(31).jpg', 'scetchbook/(32).jpg',
          'scetchbook/(33).jpg', 'scetchbook/(34).jpg', 'scetchbook/(35).jpg', 'scetchbook/(36).jpg',
          'scetchbook/(37).jpg', 'scetchbook/(38).jpg', 'scetchbook/(39).jpg', 'scetchbook/(40).jpg']

zozi = ['2021/0.jpg', '2021/1.jpg']

zozo = ['2020/(1).jpg', '2020/(2).jpg', '2020/(3).jpg', '2020/(4).jpg', '2020/(5).jpg', '2020/(6).jpg',
        '2020/(7).jpg', '2020/(8).jpg', '2020/(9).jpg', '2020/(10).jpg', '2020/(11).jpg', '2020/(12).jpg',
        '2020/(13).jpg', '2020/(14).jpg', '2020/(15).jpg', '2020/(16).jpg', '2020/(17).jpg', '2020/(18).jpg',
        '2020/(19).jpg', '2020/(20).jpg', '2020/(21).jpg', '2020/(22).jpg', '2020/(23).jpg', '2020/(24).jpg',
        '2020/(25).jpg', '2020/(26).jpg', '2020/(27).jpg', '2020/(28).jpg', '2020/(29).jpg', '2020/(30).jpg',
        '2020/(31).jpg', '2020/(32).jpg', '2020/(33).jpg', '2020/(34).jpg', '2020/(35).jpg', '2020/(36).jpg',
        '2020/(37).jpg', '2020/(38).jpg', '2020/(39).jpg', '2020/(40).jpg', '2020/(41).jpg', '2020/(42).jpg',
        '2020/(43).jpg', '2020/(44).jpg', '2020/(45).jpg', '2020/(46).jpg', '2020/(47).jpg']

zoij = ['2019/(1).jpg', '2019/(2).jpg', '2019/(3).jpg', '2019/(4).jpg',
        '2019/(5).jpg', '2019/(6).jpg', '2019/(7).jpg', '2019/(8).jpg',
        '2019/(9).jpg', '2019/(10).jpg', '2019/(11).jpg', '2019/(12).jpg',
        '2019/(13).jpg', '2019/(14).jpg', '2019/(15).jpg', '2019/(16).jpg',
        '2019/(17).jpg', '2019/(18).jpg', '2019/(19).jpg', '2019/(20).jpg',
        '2019/(21).jpg', '2019/(22).jpg', '2019/(23).jpg', '2019/(24).jpg']

zoib = ['2018/(1).jpg', '2018/(2).jpg', '2018/(3).jpg', '2018/(4).jpg', '2018/(5).jpg', '2018/(6).jpg',
        '2018/(7).jpg', '2018/(8).jpg', '2018/(9).jpg', '2018/(10).jpg', '2018/(11).jpg', '2018/(12).jpg',
        '2018/(13).jpg', '2018/(14).jpg', '2018/(15).jpg', '2018/(16).jpg', '2018/(17).jpg', '2018/(18).jpg',
        '2018/(19).jpg', '2018/(20).jpg', '2018/(21).jpg', '2018/(22).jpg', '2018/(23).jpg', '2018/(24).jpg']

zoif = ['2017/(1).jpg', '2017/(2).jpg', '2017/(3).jpg', '2017/(4).jpg', '2017/(5).jpg', '2017/(6).jpg',
        '2017/(7).jpg', '2017/(8).jpg', '2017/(9).jpg', '2017/(10).jpg', '2017/(11).jpg', '2017/(12).jpg',
        '2017/(13).jpg', '2017/(14).jpg', '2017/(15).jpg', '2017/(16).jpg', '2017/(17).jpg', '2017/(18).jpg',
        '2017/(19).jpg', '2017/(20).jpg', '2017/(21).jpg']

zois = ['2016/(1).jpg', '2016/(2).jpg', '2016/(3).jpg', '2016/(4).jpg', '2016/(5).jpg', '2016/(6).jpg',
        '2016/(7).jpg', '2016/(8).jpg', '2016/(9).jpg', '2016/(10).jpg', '2016/(11).jpg', '2016/(12).jpg',
        '2016/(13).jpg', '2016/(14).jpg', '2016/(15).jpg', '2016/(16).jpg', '2016/(17).jpg', '2016/(18).jpg',
        '2016/(19).jpg', '2016/(20).jpg', '2016/(21).jpg', '2016/(22).jpg', '2016/(23).jpg', '2016/(24).jpg',
        '2016/(25).jpg', '2016/(26).jpg']


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def main():
    global photos
    return render_template('main.html', photos=photos, title="Heillos")


def name(session, idd):
    for i in session.query(User).filter(User.id == idd):
        return i.name


def surname(session, idd):
    for i in session.query(User).filter(User.id == idd):
        return i.surname


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == "POST":
        print('post')
        if form.password.data != form.password_again.data:
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('reg.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def lin():
    form = LoginForm()
    if request.method == "POST":  # form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/albums', methods=['GET', 'POST'])
def albums():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    global photos
    return render_template('albums_list.html', title="Heillos")


@app.route('/scetchbook', methods=['GET', 'POST'])
def scetchbook():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=scetch, title="Heillos")


@app.route('/2021', methods=['GET', 'POST'])
def z1():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zozi, title="Heillos")


@app.route('/2020', methods=['GET', 'POST'])
def z2():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zozo, title="Heillos")

@app.route('/2019', methods=['GET', 'POST'])
def z3():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zoij, title="Heillos")


@app.route('/2018', methods=['GET', 'POST'])
def z4():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zoib, title="Heillos")


@app.route('/2017', methods=['GET', 'POST'])
def z5():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zoif, title="Heillos")


@app.route('/2016', methods=['GET', 'POST'])
def z6():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=zois, title="Heillos")


@app.route('/need_login', methods=['GET', 'POST'])
def need_log():
    return render_template('need_login.html', title='Авторизуйтесь')


def main():
    db_session.global_init("db/blogs.db")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()


if __name__ == '__main__':
    main()
