# SmartGalla - Advanced Web-Based POS & Inventory Management System

SmartGalla is a fully responsive, cloud-compatible Point of Sale (POS) and Inventory Management web application. It is designed to empower small to medium retail businesses with real-time analytics, barcode scanning, and seamless checkout experiences.

## 🚀 Features

*   **Cloud-Ready Barcode Scanning:** Built-in `Html5-Qrcode` integration allows users to scan product barcodes directly from their smartphone or laptop webcam without needing external hardware or backend OpenCV libraries.
*   **Intuitive Point of Sale (POS):** A streamlined checkout interface with automatic cart calculations, manual quantity overrides, and instant receipt generation.
*   **Advanced Dashboard Analytics:** Live financial tracking with `Chart.js`, featuring interactive Line Charts (Revenue over Time) and Pie Charts (Sales by Category), filterable by timeframe (7 Days, 30 Days, All Time).
*   **Complete Inventory Management:** Full CRUD (Create, Read, Update, Delete) capabilities for Products, Categories, and Suppliers, including low-stock threshold alerts.
*   **Mobile-Optimized:** The entire frontend is built with responsive Bootstrap 5 flexbox layouts, ensuring the checkout and inventory tables are fully usable on small touchscreen devices.
*   **Secure Authentication:** Role-based access control for employees and administrators using `Flask-Login`.

## 🏗️ Architecture & Tech Stack

The application follows the **Model-View-Controller (MVC)** architectural pattern, implemented via Flask Blueprints to maintain a clean, modular, and scalable codebase.

### Backend
*   **Framework:** Python 3 / Flask
*   **Database:** SQLite (Production-ready on PythonAnywhere)
*   **ORM:** SQLAlchemy (`Flask-SQLAlchemy`)
*   **Authentication:** `Flask-Login` & `Werkzeug` Security

### Frontend
*   **Styling:** HTML5, CSS3, Bootstrap 5 (Dark Mode theme)
*   **Interactivity:** Vanilla JavaScript (ES6)
*   **Data Visualization:** Chart.js
*   **Camera Integration:** Html5-Qrcode (Frontend browser scanning)

### Modular Structure (Flask Blueprints)
The backend is split into independent domains:
*   `/app/auth`: Handles user sessions and login security.
*   `/app/dashboard`: Computes aggregate financial metrics and serves JSON APIs for Chart.js.
*   `/app/inventory`: Manages SQLite database operations for the product catalog.
*   `/app/pos`: Handles live cart interactions, product lookups by barcode, and checkout transaction commits.
*   `/app/reports`: Generates post-sale invoices and historical sales tracking.

## 📂 Project Directory Structure

```text
SmartGalla/
│
├── app/
│   ├── __init__.py           # Flask App Factory & Blueprint Registration
│   ├── extensions.py         # SQLAlchemy & LoginManager instances
│   ├── models.py             # Database Schemas (User, Product, Sale, etc.)
│   ├── auth/                 # Authentication Blueprint
│   ├── dashboard/            # Dashboard Analytics Blueprint
│   ├── inventory/            # Inventory Management Blueprint
│   ├── pos/                  # Point of Sale Blueprint
│   ├── reports/              # Invoices & Reports Blueprint
│   │
│   ├── static/               # Static Assets
│   │   ├── css/style.css     # Custom CSS tokens and UI tweaks
│   │   └── img/              # Branding and placeholders
│   │
│   └── templates/            # Jinja2 HTML Templates
│       ├── base.html         # Global Layout & Navbar
│       ├── auth/             # Login forms
│       ├── dashboard/        # Chart.js canvases & metrics
│       ├── inventory/        # Product tables & Edit modals
│       └── pos/              # Barcode scanner & Checkout cart
│
├── data/                     # SQLite Database storage directory
├── config.py                 # Environment configurations
├── requirements.txt          # Python dependencies
├── run.py                    # Local development server entry point
└── wsgi.py                   # PythonAnywhere production entry point
```

## ⚙️ Installation & Deployment

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SmartGalla.git
   cd SmartGalla
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Initialize the database and run the app:
   ```bash
   python run.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.

### PythonAnywhere Deployment
1. Upload the project files to your PythonAnywhere files directory.
2. Ensure the `/data` folder exists and has write permissions.
3. In your PythonAnywhere Web tab, set the **Source code** path to your project folder.
4. Set the **WSGI configuration file** to point to the `wsgi.py` file included in this repository.
5. Click **Reload** and navigate to your cloud domain.

## 🔒 Security Notes
*   Ensure that the `SECRET_KEY` in `config.py` is overridden with a secure, randomized string in production environments.
*   The application assumes a secure HTTPS connection when deployed so that the browser can grant camera permissions for the barcode scanner. PythonAnywhere provides HTTPS by default on user subdomains.
