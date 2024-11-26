import pytest

from werkzeug.security import generate_password_hash

from app import app as flask_app, db
from app.models import User, Car

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
            db.session.refresh(user)
            return user
    return _add_user


@pytest.fixture
def add_car(app):
    """Фикстура для создания тестовой машины."""
    def _add_car(brand="Test Car", price=12, photo_path="path/to/photo"):
        with app.app_context():
            car = Car(brand=brand, price=price, photo_path=photo_path)
            db.session.add(car)
            db.session.commit()
            db.session.refresh(car)
            return car
    return _add_car

@pytest.fixture
def login_user(client, add_user):
    """Фикстура для авторизации пользователя."""
    user = add_user("testuser", "password123")
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    client.post("/login", data=login_data)
    return user