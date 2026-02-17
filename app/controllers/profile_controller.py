from flask import Blueprint

profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/')
def view():
    return "Profile page coming soon", 200