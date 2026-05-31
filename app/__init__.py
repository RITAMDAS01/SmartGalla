from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    from app.pos import pos_bp
    app.register_blueprint(pos_bp, url_prefix='/pos')

    from app.reports import reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app
