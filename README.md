# Smart Inventory Management System

A complete Inventory Management System and Point of Sale (POS) application built for small retail shops. It features a responsive modern UI (Bootstrap 5), secure authentication, webcam barcode scanning, and PDF invoice generation.

## Tech Stack
- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Database**: SQLite (No external server required)
- **Barcode Scanning**: OpenCV + Pyzbar
- **PDF Generation**: ReportLab

## Features
- **User Roles**: Admin and Employee roles with secure login (hashed passwords).
- **Dashboard**: Real-time stats, low-stock alerts, and a revenue chart.
- **Inventory CRUD**: Manage Products, Categories, and Suppliers.
- **Point of Sale (POS)**: Build carts by searching or scanning barcodes directly from your webcam.
- **Auto-Update**: Stock quantities decrease automatically upon checkout.
- **Reporting**: Generate PDF Invoices and export sales data to CSV.

## Project Structure
The app is modularized using **Flask Blueprints** for scalability:
- `app/auth`: Login and session management.
- `app/dashboard`: Analytics and charts.
- `app/inventory`: Product, category, and supplier management.
- `app/pos`: Billing, cart system, and barcode scanning logic.
- `app/reports`: Sales history, inventory logs, CSV export, and PDF generation.

## Database Schema
- **User**: `id`, `username`, `password_hash`, `role`
- **Category**: `id`, `name`, `description`
- **Supplier**: `id`, `name`, `contact`, `address`
- **Product**: `id`, `name`, `barcode`, `category_id`, `supplier_id`, `purchase_price`, `selling_price`, `stock_quantity`, `min_stock_alert`
- **Sale**: `id`, `user_id`, `total_amount`, `timestamp`
- **SaleItem**: `id`, `sale_id`, `product_id`, `quantity`, `price_at_time_of_sale`
- **InventoryLog**: `id`, `product_id`, `change_amount`, `reason`, `timestamp`

## Setup Guide

### 1. Requirements
- Python 3.8+
- Webcam (required for barcode scanning feature)

### 2. Installation
Clone the project or navigate to the directory, then run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database & Sample Data
You can populate the database with dummy categories, suppliers, and products to test the system:

```bash
python populate_db.py
```

### 4. Run the Application
Start the Flask server:

```bash
python run.py
```

Navigate to `http://localhost:5000` in your web browser.

**Default Login:**
- Username: `admin`
- Password: `admin`

## Running Locally for Free
Because this uses SQLite, all database information is saved into a local file (`data/inventory.db`). There are no external databases, servers, or paid APIs required. It runs completely offline on your localhost.
