from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    
    username = db.Column(db.String(255), index=True, unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    userinfo = db.relationship('UserInfo', backref='user', uselist=False)  # Связь с UserInfo

    def __repr__(self):
        return f'{self.id}:{self.username}'


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer(), primary_key=True)
    
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'{self.id}:{self.first_name}'


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer(), primary_key=True)

    brand = db.Column(db.String(255))
    price = db.Column(db.Integer)
    photo_path = db.Column(db.String(255))

    def __repr__(self):
        return f'{self.id}'



class UserRent(db.Model):
    __tablename__ = 'user_rent'
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

    car = db.relationship('Car', backref='rents')

    def __repr__(self):
        return f'{self.id}'
