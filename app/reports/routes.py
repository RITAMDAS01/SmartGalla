from flask import render_template, request, Response, make_response
from flask_login import login_required
from app.reports import reports_bp
from app.models import Sale, InventoryLog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
import csv

@reports_bp.route('/')
@login_required
def index():
    recent_sales = Sale.query.order_by(Sale.timestamp.desc()).limit(20).all()
    logs = InventoryLog.query.order_by(InventoryLog.timestamp.desc()).limit(20).all()
    return render_template('reports/index.html', sales=recent_sales, logs=logs)

@reports_bp.route('/invoice/<int:sale_id>')
@login_required
def invoice(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    
    # Generate PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, height - 50, "SmartGalla - Invoice")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Invoice Number: #{sale.id}")
    p.drawString(50, height - 95, f"Date: {sale.timestamp.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(50, height - 110, f"Served By: {sale.user.username}")
    
    # Table Header
    y = height - 150
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Product")
    p.drawString(300, y, "Price")
    p.drawString(400, y, "Qty")
    p.drawString(500, y, "Total")
    p.line(50, y-5, 550, y-5)
    
    # Table Rows
    y -= 25
    p.setFont("Helvetica", 12)
    for item in sale.items:
        p.drawString(50, y, item.product.name[:35])
        p.drawString(300, y, f"Rs.{item.price_at_time_of_sale:.2f}")
        p.drawString(400, y, str(item.quantity))
        p.drawString(500, y, f"Rs.{(item.price_at_time_of_sale * item.quantity):.2f}")
        y -= 20
        
    p.line(50, y, 550, y)
    y -= 20
    p.setFont("Helvetica-Bold", 14)
    p.drawString(400, y, "Total Amount:")
    p.drawString(500, y, f"Rs.{sale.total_amount:.2f}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=invoice_{sale.id}.pdf'
    return response

@reports_bp.route('/export_csv')
@login_required
def export_csv():
    sales = Sale.query.all()
    
    def generate():
        data = io.StringIO()
        writer = csv.writer(data)
        
        # Header
        writer.writerow(['Sale ID', 'Date', 'User', 'Total Amount', 'Items Count'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        for sale in sales:
            writer.writerow([sale.id, sale.timestamp, sale.user.username, sale.total_amount, sale.items.count()])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
            
    response = Response(generate(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=sales_report.csv'
    return response
