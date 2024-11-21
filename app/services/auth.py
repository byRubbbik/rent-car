# Функции для авторизации и регистрации
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User


def auth(loginform):
    user = User.query.filter_by(username=loginform["username"]).first()
    if user and check_password_hash(user.password, loginform["password"]):
        return user
    return False


def register(regform):
    if not User.query.filter_by(username=regform["username"]).first():
        try:
            hash = generate_password_hash(regform["password"])            
            users = User(username=regform["username"], password=hash)
            
            db.session.add(users)
            db.session.commit()
            return User.query.filter_by(username=regform["username"]).first()
        except:
            db.session.rollback()
            return False