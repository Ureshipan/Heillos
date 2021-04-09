from flask import Flask, request, render_template, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
import flask

import datetime
from data import db_session
from data.users import User
from data.login_form import LoginForm
from data.register import RegisterForm


photos = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', ]

scetch = ['scetchbook/ (1).jpg', 'scetchbook/ (2).jpg', 'scetchbook/ (3).jpg', 'scetchbook/ (4).jpg',
          'scetchbook/ (5).jpg', 'scetchbook/ (6).jpg', 'scetchbook/ (7).jpg', 'scetchbook/ (8).jpg',
          'scetchbook/ (9).jpg', 'scetchbook/ (10).jpg', 'scetchbook/ (11).jpg', 'scetchbook/ (12).jpg',
          'scetchbook/ (13).jpg', 'scetchbook/ (14).jpg', 'scetchbook/ (15).jpg', 'scetchbook/ (16).jpg',
          'scetchbook/ (17).jpg', 'scetchbook/ (18).jpg', 'scetchbook/ (19).jpg', 'scetchbook/ (20).jpg',
          'scetchbook/ (21).jpg', 'scetchbook/ (22).jpg', 'scetchbook/ (23).jpg', 'scetchbook/ (24).jpg',
          'scetchbook/ (25).jpg', 'scetchbook/ (26).jpg', 'scetchbook/ (27).jpg', 'scetchbook/ (28).jpg',
          'scetchbook/ (29).jpg', 'scetchbook/ (30).jpg', 'scetchbook/ (31).jpg', 'scetchbook/ (32).jpg',
          'scetchbook/ (33).jpg', 'scetchbook/ (34).jpg', 'scetchbook/ (35).jpg', 'scetchbook/ (36).jpg',
          'scetchbook/ (37).jpg', 'scetchbook/ (38).jpg', 'scetchbook/ (39).jpg', 'scetchbook/ (40).jpg']


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
    if request.method == "POST":#form.validate_on_submit():
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
def album():
    if not current_user.is_authenticated:
        return redirect('/need_login')
    return render_template('album_present.html', photos=scetch, title="Heillos")

@app.route('/need_login', methods=['GET', 'POST'])
def need_log():
    return render_template('need_login.html', title='Авторизуйтесь')

def main():
    db_session.global_init("db/blogs.db")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()


if __name__ == '__main__':
    main()
