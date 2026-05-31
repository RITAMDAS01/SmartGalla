from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='Employee') # Admin or Employee
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    products = db.relationship('Product', backref='category', lazy='dynamic')

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    contact = db.Column(db.String(64))
    address = db.Column(db.String(256))
    products = db.relationship('Product', backref='supplier', lazy='dynamic')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    barcode = db.Column(db.String(64), unique=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    purchase_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    min_stock_alert = db.Column(db.Integer, default=10)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('SaleItem', backref='sale', lazy='dynamic')
    user = db.relationship('User', backref='sales')

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time_of_sale = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    change_amount = db.Column(db.Integer, nullable=False) # positive for restock, negative for sale
    reason = db.Column(db.String(64)) # e.g. "Sale", "Restock", "Manual Edit"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    product = db.relationship('Product')
