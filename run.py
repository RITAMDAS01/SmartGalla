from app import create_app
from app.extensions import db
from app.models import User, Category, Supplier, Product, Sale, SaleItem, InventoryLog
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Category': Category, 'Supplier': Supplier, 
            'Product': Product, 'Sale': Sale, 'SaleItem': SaleItem, 'InventoryLog': InventoryLog}

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)
    
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='Admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created (admin/admin).")

    app.run(debug=True)
