import re
import random
import string
from flask import flash, url_for
from flask_mail import Message
from app.extensions import mail


# ============== VALIDATION FUNCTIONS ==============

def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    
    return True, ""


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def validate_phone(phone):
    """Validate phone number (optional field)"""
    if not phone:
        return True, ""  # Phone is optional
    
    phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
    if not re.match(phone_regex, phone.replace('-', '').replace(' ', '')):
        return False, "Invalid phone number format"
    
    return True, ""


def validate_username(username):
    """Validate username"""
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""


# ============== OTP FUNCTIONS ==============

def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))


# ============== EMAIL FUNCTIONS ==============

def send_otp_email(email, otp_code, username):
    """Send OTP email for password reset"""
    try:
        msg = Message(
            subject='QuickStay - Password Reset OTP',
            recipients=[email]
        )
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .otp-box {{ background: #f4f4f4; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; }}
                .footer {{ margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Password Reset Request</h2>
                <p>Hello {username},</p>
                <p>You requested to reset your password. Use the OTP code below:</p>
                
                <div class="otp-box">{otp_code}</div>
                
                <p><strong>This code will expire in 10 minutes.</strong></p>
                
                <p>If you didn't request this, please ignore this email.</p>
                
                <div class="footer">
                    <p>© 2026 QuickStay. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        return True, "OTP sent successfully"
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


def send_welcome_email(email, username):
    """Send welcome email after registration"""
    try:
        msg = Message(
            subject='Welcome to QuickStay!',
            recipients=[email]
        )
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ margin-top: 20px; font-size: 12px; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to QuickStay!</h1>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    <p>Thank you for registering with QuickStay. Your account has been successfully created!</p>
                    <p>You can now:</p>
                    <ul>
                        <li>Browse available rooms</li>
                        <li>Make bookings</li>
                        <li>Manage your profile</li>
                        <li>Leave reviews</li>
                    </ul>
                    <p>If you have any questions, feel free to contact our support team.</p>
                </div>
                <div class="footer">
                    <p>© 2026 QuickStay. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        return True, "Welcome email sent"
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"
    
def send_password_reset_confirmation_email(email, username):
    """Send confirmation email after password reset"""
    try:
        from datetime import datetime
        
        msg = Message(
            subject='QuickStay - Password Reset Successful',
            recipients=[email]
        )
        
        current_time = datetime.utcnow().strftime('%B %d, %Y at %I:%M %p UTC')
        
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4F46E5; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .success-icon {{ font-size: 48px; margin-bottom: 10px; }}
                .info-box {{ background: #fff; border-left: 4px solid #4F46E5; padding: 15px; margin: 20px 0; }}
                .warning-box {{ background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 15px; margin: 20px 0; }}
                .button {{ display: inline-block; background: #4F46E5; color: #ffffff !important; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; font-weight: bold; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="success-icon">🔐</div>
                    <h1>Password Reset Successful</h1>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    
                    <p>Your password has been successfully reset on <strong>{current_time}</strong>.</p>
                    
                    <div class="info-box">
                        <strong>✅ What happened:</strong>
                        <p style="margin: 5px 0 0 0;">Your QuickStay account password was changed. You can now log in with your new password.</p>
                    </div>
                    
                    <div class="warning-box">
                        <strong>⚠️ Didn't make this change?</strong>
                        <p style="margin: 5px 0 0 0;">If you didn't reset your password, please contact our support team immediately or reset your password again to secure your account.</p>
                    </div>
                    
                    <center>
                        <a href="{url_for('auth.login')}" class="button" style="color: #ffffff !important;">Login to Your Account</a>
                    </center>
                    
                    <div class="footer">
                        <p>This is an automated security notification from QuickStay.</p>
                        <p>© 2026 QuickStay. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(msg)
        return True, "Password reset confirmation email sent"
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"