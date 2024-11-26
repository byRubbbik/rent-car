import pytest

from werkzeug.security import generate_password_hash

from app import app as flask_app, db
from app.models import User

from config import Config


@pytest.fixture
def app():
    """Фикстура для тестового приложения Flask."""
    flask_app.config.from_object(Config)
    flask_app.config['TESTING'] = True
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Фикстура для тестового клиента Flask."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Фикстура для тестового CLI Flask."""
    return app.test_cli_runner()


@pytest.fixture
def add_user(app):
    """Фикстура для создания тестового пользователя."""
    def _add_user(username, password):
        with app.app_context():
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit() 
            return user
    return _add_user

