from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from secrets import token_hex
from werkzeug.security import generate_password_hash

# Instantiate the database
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable = False,unique=True)
    email = db.Column(db.String(100),nullable = False,unique=True)
    password = db.Column(db.String,nullable=False)
    date_joined = db.Column(db.DateTime,nullable = False, default=datetime.utcnow())
    apitoken = db.Column(db.String,unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'apitoken': self.apitoken
        }

    def __init__(self, username,email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable = False, unique=True)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(500), nullable = False)
    image_url = db.Column(db.String)

    # associated_carts = db.relationship("Carts",foreign_keys='Carts.product_id',back_populates="product")

    def __init__(self, product_name, price, description, image_url):
        self.product_name = product_name
        self.price = price
        self.description = description
        self.image_url = image_url

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    
class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_quantity = db.Column(db.Integer,nullable=False)
    
    # user_id = db.Column(db.Integer, db.ForeignKey(Users.id),nullable=False)
    # user = db.relationship("Users",back_populates="cart_items",foreign_keys=[user_id])
    
    # product_id = db.Column(db.Integer, db.ForeignKey(Products.id),nullable=False)
    # product = db.relationship("Products",back_populates="associated_carts",foreign_keys=[product_id])
    
    def __init__(self, user_id, product_id, item_quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.item_quantity = item_quantity

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    
    
