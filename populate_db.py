from app import create_app
from app.extensions import db
from app.models import Category, Supplier, Product, User
import random

app = create_app()

def populate():
    with app.app_context():
        # Ensure db exists
        db.create_all()

        # Admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='Admin')
            admin.set_password('admin')
            db.session.add(admin)

        # Categories
        if not Category.query.first():
            c1 = Category(name='Electronics', description='Gadgets and devices')
            c2 = Category(name='Groceries', description='Daily food items')
            c3 = Category(name='Clothing', description='Apparel and accessories')
            db.session.add_all([c1, c2, c3])
            db.session.commit()
            
            # Suppliers
            s1 = Supplier(name='TechCorp', contact='contact@techcorp.com', address='Silicon Valley')
            s2 = Supplier(name='FreshFarms', contact='fresh@farms.com', address='Countryside')
            db.session.add_all([s1, s2])
            db.session.commit()

            # Products
            p1 = Product(name='Wireless Mouse', barcode='1234567890', category_id=c1.id, supplier_id=s1.id, purchase_price=10.0, selling_price=25.0, stock_quantity=50)
            p2 = Product(name='Mechanical Keyboard', barcode='0987654321', category_id=c1.id, supplier_id=s1.id, purchase_price=45.0, selling_price=90.0, stock_quantity=5)
            p3 = Product(name='Apple', barcode='111222333', category_id=c2.id, supplier_id=s2.id, purchase_price=0.5, selling_price=1.2, stock_quantity=200)
            p4 = Product(name='Milk (1L)', barcode='444555666', category_id=c2.id, supplier_id=s2.id, purchase_price=1.5, selling_price=2.5, stock_quantity=0) # Out of stock
            
            db.session.add_all([p1, p2, p3, p4])
            db.session.commit()
            print("Successfully populated the database with sample data!")
        else:
            print("Database already contains data. Skipping population.")

if __name__ == '__main__':
    populate()
