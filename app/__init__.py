from flask import Flask, render_template
from .config import config
from .extensions import db, migrate, login_manager, mail, csrf


def create_app(config_name='default'):
    """
    App Factory Function
    """

    # 1. Create Flask app
    app = Flask(__name__)

    # 2. Load config
    app.config.from_object(config[config_name])

    # 3. Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # 4. Register blueprints
    _register_blueprints(app)

    # 5. Register error handlers
    _register_error_handlers(app)

    # 6. Setup login manager
    _setup_login_manager()

    # 7. Import models
    with app.app_context():
        from . import models

    return app


def _register_blueprints(app):
    """Register all blueprints (controllers)"""
    try:
        from .controllers.main_controller import main
        from .controllers.auth_controller import auth
        from .controllers.profile_controller import profile
        from .controllers.booking_controller import booking
        from .controllers.admin.dashboard_controller import admin_dashboard

        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(profile)
        app.register_blueprint(booking)
        app.register_blueprint(admin_dashboard)

    except Exception as e:
        print(f"Error registering blueprints: {e}")


def _register_error_handlers(app):
    """Register custom error pages"""

    @app.errorhandler(404)
    def not_found(error):
        try:
            return render_template('extra/404.html'), 404
        except Exception:
            return "Page not found", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "Internal server error", 500


def _setup_login_manager():
    """Configure Flask-Login user loader"""

    @login_manager.user_loader
    def load_user(user_id):
        try:
            from .models.user import User
            return User.query.get(int(user_id))
        except Exception as e:
            return None