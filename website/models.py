from sqlalchemy import event
from . import db
from sqlalchemy import DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tovar(db.Model):
    __tablename__ = 'tovar'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default='Mat', nullable=False)
    name = db.Column(db.String(150), unique=True)
    count = db.Column(db.Integer)
    cost = db.Column(db.Float)
    status = db.Column(db.String(20))
    color = db.Column(db.String(30))
    size = db.Column(db.String(20))
    thickness = db.Column(db.String(20)) 
    material = db.Column(db.String(20)) 
    base = db.Column(db.String(20))
    info = db.Column(db.String(500))
    img_name = db.Column(db.String(500), unique=True)
    
    order = db.relationship('Order', backref='orders', lazy=True, cascade="all, delete-orphan")

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    nomerzakaza = db.Column(db.Integer)
    fio = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    track_number = db.Column(db.String(200), default='Soon')
    receiving_point = db.Column(db.String(150), db.ForeignKey('point.id'))
    country = db.Column(db.String(30), default='Belarus')
    city = db.Column(db.String(20))
    street = db.Column(db.String(100))
    house = db.Column(db.String(10))
    flat = db.Column(db.String(10))
    comment = db.Column(db.String(200))
    promocod = db.Column(db.String(10))
    tovar_id = db.Column(db.Integer, db.ForeignKey('tovar.id'), nullable=False)
    price = db.Column(db.Float)
    tovar_quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='In processing')
    created_at = db.Column(DateTime, default=datetime.now)
    
    point = db.relationship('Point', backref='order', lazy=True)
    tovar = db.relationship('Tovar', backref='orders', lazy=True)

class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    street = db.Column(db.String)
    number = db.Column(db.Integer)
    
    orders = db.relationship('Order', backref='receiving_point_rel', lazy=True)
