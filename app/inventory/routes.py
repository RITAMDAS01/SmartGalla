from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.inventory import inventory_bp
from app.inventory.forms import CategoryForm, SupplierForm, ProductForm
from app.models import Category, Supplier, Product
from app.extensions import db
import uuid
import cv2
import zxingcpp
import time

@inventory_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('inventory.categories'))
    categories = Category.query.all()
    return render_template('inventory/categories.html', categories=categories, form=form)

@inventory_bp.route('/suppliers', methods=['GET', 'POST'])
@login_required
def suppliers():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(name=form.name.data, contact=form.contact.data, address=form.address.data)
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully.', 'success')
        return redirect(url_for('inventory.suppliers'))
    suppliers = Supplier.query.all()
    return render_template('inventory/suppliers.html', suppliers=suppliers, form=form)

@inventory_bp.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        barcode = form.barcode.data
        if not barcode:
            barcode = str(uuid.uuid4().hex)[:10].upper()
            
        product = Product(
            name=form.name.data,
            barcode=barcode,
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data,
            purchase_price=form.purchase_price.data,
            selling_price=form.selling_price.data,
            stock_quantity=form.stock_quantity.data,
            min_stock_alert=form.min_stock_alert.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('inventory.products'))
        
    products = Product.query.all()
    return render_template('inventory/products.html', products=products, form=form)

@inventory_bp.route('/scan_raw', methods=['POST'])
@login_required
def scan_raw():
    cap = cv2.VideoCapture(0)
    time.sleep(1) # warm up camera
    ret, frame = cap.read()
    cap.release()

    if not ret:
        from flask import jsonify
        return jsonify({'error': 'Failed to capture image from camera'}), 500

    barcodes = zxingcpp.read_barcodes(frame)
    if not barcodes:
        from flask import jsonify
        return jsonify({'error': 'No barcode found in frame'}), 404

    from flask import jsonify
    return jsonify({'barcode': barcodes[0].text})
