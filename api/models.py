from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, server_default='100')  
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())

    # Define the relationship with images
    images = db.relationship('ProductImage', backref='product', lazy=True)

class ProductImage(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_name = db.Column(db.String(250), nullable=False)
    image_url = db.Column(db.String(250), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    county=db.Column(db.String, nullable=False)
    sub_county=db.Column(db.String, nullable=False)
    ward=db.Column(db.String, nullable=False)
    street=db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('Pending', 'Processing', 'Completed',name="status"), default='Pending')
    order_date = db.Column(db.DateTime, server_default=db.func.now())
    product_ids = db.Column(db.String, nullable=False)

class OrderProduct(db.Model):

    __tablename__ = "order_products"
    id = db.Column(db.Integer, primary_key=True)
    product_id= db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    quantity= db.Column(db.Integer, nullable=False)

    # Define relationship with Product
    product = db.relationship('Product', backref='order_products')

class Admins(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now())
