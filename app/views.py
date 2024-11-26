from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, login_user, current_user, logout_user

from app import app
from app.models import User, UserInfo, Car, UserRent
from app.services.forms import reg_forms, login_forms, user_info_forms

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/catalog")
@login_required
def catalog():
    car = Car.query.all()
    return render_template('catalog.html', cars=car)

# FOR AUTH
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        regform = {
            "username": request.form.get('username'),
            "password": request.form.get('password')
        }
        result = reg_forms(regform=regform)
        if result:
            if result == 1:
                flash("Пароль должен состоять из 8 и более символов")
            else:
                login_user(result)
                if not current_user.userinfo:
                    return redirect(url_for('profile', username=current_user.username))
        else:
            flash('Проверьте поля ввода')
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        loginform = {
            "username": request.form.get('username'),
            "password": request.form.get('password')
        }
        result = login_forms(loginform=loginform)
        if result:
            login_user(result)
            if current_user.is_authenticated:
                return redirect(url_for('profile', username=current_user.username))
        else:
            flash('Проверьте поля ввода')
    return render_template("login.html")


@app.route('/profile/add_userinfo/<id>', methods=["GET", "POST"])
def add_userinfo(id):
    if request.method == "POST":
        user_info = {
            "id": id,
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone_number": request.form.get("phone_number"),
            "email": request.form.get("email")
        }
        
        response = user_info_forms(user_info)
        
        if response:
            if not current_user.userinfo:
                return redirect(url_for('add_userinfo', id=current_user.id))  # Редирект на страницу добавления информации
            else:
                return redirect(url_for('profile', username=current_user.username))
        else:
            flash("Проверьте поля ввода")

    return render_template("add_userinfo.html")


@app.route('/profile/<username>', methods=['POST', 'GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user != current_user:
        abort(403)

    userinfo = UserInfo.query.filter_by(user_id=user.id).first()
    if not userinfo or not userinfo.first_name or not userinfo.last_name:
        return redirect(url_for('add_userinfo', id=user.id))
    
    rents = UserRent.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', rents=rents, userinfo=userinfo)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 
