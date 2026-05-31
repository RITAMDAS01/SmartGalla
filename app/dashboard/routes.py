from flask import render_template
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp
from app.models import Product, Sale, Supplier, Category
from datetime import datetime, timedelta

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_products = Product.query.count()
    total_categories = Category.query.count()
    low_stock_items = Product.query.filter(Product.stock_quantity <= Product.min_stock_alert).count()
    out_of_stock_items = Product.query.filter_by(stock_quantity=0).count()
    
    # Calculate revenue
    today = datetime.utcnow().date()
    # Using python to filter for sqlite compatibility in simple queries
    all_sales = Sale.query.all()
    today_sales = [s for s in all_sales if s.timestamp.date() == today]
    today_revenue = sum(s.total_amount for s in today_sales)
    
    total_revenue = sum(s.total_amount for s in all_sales)
    
    # Top 5 low stock products for the table
    low_stock_list = Product.query.filter(Product.stock_quantity <= Product.min_stock_alert).order_by(Product.stock_quantity.asc()).limit(5).all()
    
    return render_template('dashboard/index.html', 
                           total_products=total_products,
                           total_categories=total_categories,
                           low_stock_items=low_stock_items,
                           out_of_stock_items=out_of_stock_items,
                           today_revenue=today_revenue,
                           total_revenue=total_revenue,
                           low_stock_list=low_stock_list)
