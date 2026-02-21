from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.utils import (
    validate_email, 
    validate_password, 
    validate_phone, 
    validate_username,
    generate_otp,
    send_otp_email,
    send_welcome_email,
    send_password_reset_confirmation_email
)

auth = Blueprint('auth', __name__, url_prefix='/auth')

# ============== REGISTRATION ==============

@auth.route('/register', methods=['GET', 'POST'])
def register():
    try:
        # If user is already logged in, redirect to home
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('main.home'))
        
        if request.method == 'POST':
            # Get form data
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            # Validation
            errors = []
            
            # First name validation
            if not first_name:
                errors.append('First name is required')
            elif len(first_name) < 2:
                errors.append('First name must be at least 2 characters')
            
            # Username validation
            is_valid, msg = validate_username(username)
            if not is_valid:
                errors.append(msg)
            
            # Email validation
            is_valid, msg = validate_email(email)
            if not is_valid:
                errors.append(msg)
            
            # Phone validation (optional)
            is_valid, msg = validate_phone(phone)
            if not is_valid:
                errors.append(msg)
            
            # Password validation
            is_valid, msg = validate_password(password)
            if not is_valid:
                errors.append(msg)
            
            # Confirm password
            if password != confirm_password:
                errors.append('Passwords do not match')
            
            # Check if username already exists
            if User.query.filter_by(username=username).first():
                errors.append('Username already exists')
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                errors.append('Email already registered')
            
            # If there are errors, flash them and return
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('auth/register.html')
            
            # Create new user
            try:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name if last_name else None,
                    username=username,
                    email=email,
                    phone=phone if phone else None,
                    role='user'
                )
                new_user.set_password(password)
                
                # Save to database
                db.session.add(new_user)
                db.session.commit()
                
                # Send welcome email (optional - won't block registration if it fails)
                send_welcome_email(email, username)
                
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
                
            except Exception as e:
                db.session.rollback()
                flash('An error occurred during registration. Please try again.', 'danger')
                print(f"Registration error: {str(e)}")
                return render_template('auth/register.html')
        
        # GET request - show registration form
        return render_template('auth/register.html')
    
    except Exception as e:
        print(f"Error in register route: {str(e)}")
        abort(500)

# ============== LOGIN ==============

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('main.home'))
        
        if request.method == 'POST':
            username_or_email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            remember_me = request.form.get('remember') == 'on'
            errors = []
            
            if not username_or_email:
                errors.append('Username or email is required')
            
            if not password:
                errors.append('Password is required')
            
            # If there are errors, flash them and return
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('auth/login.html')
            
            user = User.query.filter(
                (User.username == username_or_email) | 
                (User.email == username_or_email.lower())
            ).first()
            
            if not user or not user.check_password(password):
                flash('Invalid username/email or password', 'danger')
                return render_template('auth/login.html')
            
            # Check if user account is active
            if user.is_blocked():
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember_me)
            
            flash(f'Welcome back, {user.get_full_name()}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        
        # GET request - show login form
        return render_template('auth/login.html')
    
    except Exception as e:
        print(f"Error in login route: {str(e)}")
        flash('Something went wrong. Please try again.', 'danger')
        return render_template('auth/login.html')
    
# ============== LOGOUT ==============

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('main.home'))
    except Exception as e:
        abort(500)

# ============== FORGOT PASSWORD - 4 Stages ==============

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Stage 1: Request OTP - User enters email"""
    try:
        # If user is already logged in, redirect
        if current_user.is_authenticated:
            flash('You are already logged in.', 'info')
            return redirect(url_for('main.home'))
        
        # POST request - Handle form submission
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            
            print(f"🔍 DEBUG: Received email: {email}")  # Debug log
            
            # Validate email
            is_valid, msg = validate_email(email)
            if not is_valid:
                return {'success': False, 'message': msg}, 400
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            print(f"🔍 DEBUG: User found: {user}")  # Debug log
            
            if not user:
                return {'success': True, 'message': 'If this email exists, an OTP has been sent.'}, 200
            
            # Check if user account is active
            if user.is_blocked():
                return {'success': False, 'message': 'Your account has been deactivated. Contact support.'}, 403
            
            # Generate OTP
            otp_code = generate_otp()
            print(f"🔍 DEBUG: Generated OTP: {otp_code}")  # Debug log
            
            # Save OTP to database
            try:
                user.set_otp(otp_code)
                db.session.commit()
                print(f"✅ DEBUG: OTP saved to database")  # Debug log
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error saving OTP: {str(e)}")
                return {'success': False, 'message': 'Failed to generate OTP. Please try again.'}, 500
            
            # Send OTP email
            success, message = send_otp_email(email, otp_code, user.get_full_name())
            print(f"📧 DEBUG: Email result - Success: {success}, Message: {message}")  # Debug log
            
            if not success:
                return {'success': False, 'message': 'Failed to send OTP email. Please try again.'}, 500
            
            # Store email in session for next steps
            from flask import session
            session['reset_email'] = email
            
            return {'success': True, 'message': 'OTP sent to your email.'}, 200
        
        # GET request - show form
        return render_template('auth/forgot-password.html')
    
    except Exception as e:
        print(f"❌ Error in forgot_password route: {str(e)}")
        abort(500)

@auth.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        from flask import session

        # Get email from session
        email = session.get('reset_email')
        if not email:
            flash('Session expired. Please start over.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        otp = request.form.get('otp', '').strip()
        
        if not otp or len(otp) != 6:
            flash('Please enter a valid 6-digit OTP.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        # Verify OTP
        if not user.verify_otp(otp):
            flash('Invalid or expired OTP. Please try again.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        session['otp_verified'] = True
        
        return {'success': True, 'message': 'OTP verified successfully.'}, 200
    
    except Exception as e:
        print(f"Error in verify_otp route: {str(e)}")
        return {'success': False, 'message': 'An error occurred. Please try again.'}, 500


@auth.route('/reset-password', methods=['POST'])
def reset_password():
    """Stage 3: Reset Password - User enters new password"""
    try:
        from flask import session
        
        # Check if OTP was verified
        if not session.get('otp_verified'):
            return {'success': False, 'message': 'Please verify OTP first.'}, 400
        
        # Get email from session
        email = session.get('reset_email')
        if not email:
            return {'success': False, 'message': 'Session expired. Please start over.'}, 400
        
        # Get passwords from form
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_new_password', '').strip()
        
        # Validate password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return {'success': False, 'message': msg}, 400
        
        # Check if passwords match
        if new_password != confirm_password:
            return {'success': False, 'message': 'Passwords do not match.'}, 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {'success': False, 'message': 'User not found.'}, 404
        
        # Update password
        try:
            user.set_password(new_password)
            user.clear_otp()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting password: {str(e)}")
            return {'success': False, 'message': 'Failed to reset password. Please try again.'}, 500
        
        # Send confirmation email (non-blocking - won't fail the reset if email fails)
        try:
            send_password_reset_confirmation_email(email, user.get_full_name())
        except Exception as e:
            print(f"Password reset confirmation email failed: {str(e)}")
            # Continue anyway - password is already reset
        
        # Clear session
        session.pop('reset_email', None)
        session.pop('otp_verified', None)
        
        return {'success': True, 'message': 'Password reset successfully!'}, 200
    
    except Exception as e:
        print(f"Error in reset_password route: {str(e)}")
        return {'success': False, 'message': 'An error occurred. Please try again.'}, 500


@auth.route('/resend-otp', methods=['POST'])
def resend_otp():
    try:
        from flask import session
        
        email = session.get('reset_email')
        if not email:
            flash('Session expired. Please start over.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        otp_code = generate_otp()
        
        try:
            user.set_otp(otp_code)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving OTP: {str(e)}")
            flash('Failed to generate OTP. Please try again.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        success, message = send_otp_email(email, otp_code, user.get_full_name())
        
        if not success:
            print(f"Email send failed: {message}")
            flash('Failed to send OTP email. Please try again.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        return {'success': True, 'message': 'New OTP sent to your email.'}, 200
    
    except Exception as e:
        print(f"Error in resend_otp route: {str(e)}")
        flash('An error occurred in sending OTP again. Please try again.', 'danger')
        return redirect(url_for('auth.forgot_password'))