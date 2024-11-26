from bs4 import BeautifulSoup

from flask import url_for

from app import db, app as flask_app
from app.models import User


def test_index(client):
    """Тест главной страницы с проверкой заголовка."""
    response = client.get(url_for('index'))
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')

    title = soup.find('title')
    assert title is not None
    assert title.text == "Главная"


def test_register(client):
    """Тест регистрации нового пользователя."""
    response = client.post(url_for('register'), data={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 302


def test_login_success(client, add_user):
    """Тест успешного входа пользователя."""
    user = add_user('testuser', 'password123')

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    

def test_login_failure(client, add_user):
    """Тест неудачного входа с неверными данными."""
    add_user('testuser', 'password123')

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200


def test_protected_route(client, add_user):
    """Тест защищенного маршрута."""
    add_user('testuser', 'password123')
    response = client.get('/catalog')
    assert response.status_code == 302

    client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    response = client.get('/catalog')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    title = soup.find('title')
    assert title is not None
    assert title.text == "Каталог автомобилей"