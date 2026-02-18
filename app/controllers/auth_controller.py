from flask import Blueprint, render_template, abort

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login():
    try:
        return render_template('auth/login.html')
    except Exception as e:
        abort(500)


@auth.route('/register')
def register():
    try:
        return render_template('auth/register.html')
    except Exception as e:
        abort(500)


@auth.route('/forgot-password')
def forgot_password():
    try:
        return render_template('auth/forgot-password.html')
    except Exception as e:
        abort(500)


@auth.route('/logout')
def logout():
    try:
        return "Logout coming soon", 200
    except Exception as e:
        abort(500)