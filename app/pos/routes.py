from flask import render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import login_required, current_user
from app.pos import pos_bp
from app.models import Product, Sale, SaleItem, InventoryLog
from app.extensions import db
import cv2
import zxingcpp
import time

@pos_bp.route('/')
@login_required
def index():
    return render_template('pos/index.html')

@pos_bp.route('/scan_barcode', methods=['POST'])
@login_required
def scan_barcode():
    # Use OpenCV to capture a frame from webcam
    cap = cv2.VideoCapture(0)
    time.sleep(1) # warm up camera
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return jsonify({'error': 'Failed to capture image from camera'}), 500

    # Decode barcode using zxingcpp
    barcodes = zxingcpp.read_barcodes(frame)
    if not barcodes:
        return jsonify({'error': 'No barcode found in frame'}), 404

    # Just take the first one
    barcode_data = barcodes[0].text
    
    # Find product in db
    product = Product.query.filter_by(barcode=barcode_data).first()
    if not product:
        return jsonify({'error': 'Product not found for barcode: ' + barcode_data}), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'barcode': product.barcode,
        'price': product.selling_price,
        'stock': product.stock_quantity
    })

@pos_bp.route('/search_product', methods=['GET'])
@login_required
def search_product():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # Simple search by name or barcode
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | 
        (Product.barcode.ilike(f'%{query}%'))
    ).limit(10).all()
    
    results = [{
        'id': p.id,
        'name': p.name,
        'barcode': p.barcode,
        'price': p.selling_price,
        'stock': p.stock_quantity
    } for p in products]
    
    return jsonify(results)

@pos_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.json
    cart = data.get('cart', [])
    
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400
        
    try:
        # Create Sale
        total_amount = sum(item['price'] * item['quantity'] for item in cart)
        sale = Sale(user_id=current_user.id, total_amount=total_amount)
        db.session.add(sale)
        db.session.flush() # Get sale.id
        
        for item in cart:
            prod = Product.query.get(item['id'])
            if not prod or prod.stock_quantity < item['quantity']:
                db.session.rollback()
                return jsonify({'error': f"Not enough stock for {item['name']}"}), 400
                
            # Deduct stock
            prod.stock_quantity -= item['quantity']
            
            # Create SaleItem
            sale_item = SaleItem(
                sale_id=sale.id, 
                product_id=prod.id, 
                quantity=item['quantity'], 
                price_at_time_of_sale=item['price']
            )
            db.session.add(sale_item)
            
            # Create Inventory Log
            log = InventoryLog(
                product_id=prod.id,
                change_amount=-item['quantity'],
                reason='Sale'
            )
            db.session.add(log)
            
        db.session.commit()
        return jsonify({'success': True, 'sale_id': sale.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
