from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config, UserLogin

# Инициализируем Flask.
app = Flask(__name__, template_folder='templates')

# Указываем местоположение класса с настройками.
app.config.from_object(Config)
app.config.from_object(UserLogin)

# Создаем обьект БД.
db = SQLAlchemy(app)

# Создаем обьект, представляющий собой механизм миграций.
migrate = Migrate(app, db)

# Создаём объект авторизации
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ."


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
    

from app import models, views
from app.api.v1 import rent