from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login')
def login():
    try:
        return render_template('auth/login.html')
    except Exception as e:
        return "Login page coming soon", 200

@auth.route('/register')
def register():
    try:
        return render_template('auth/register.html')
    except Exception as e:
        return "Register page coming soon", 200

@auth.route('/logout')
def logout():
    return "Logout coming soon", 200