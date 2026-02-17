from flask import Blueprint

admin_dashboard = Blueprint('admin_dashboard', __name__, url_prefix='/admin')

@admin_dashboard.route('/dashboard')
def dashboard():
    return "Admin dashboard coming soon", 200