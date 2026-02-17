from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # ID 
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(60), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)

    # Authentication
    password_hash = db.Column(db.String(256), nullable=False)

    # Role & Status
    role = db.Column(db.String(10), default='user', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # OTP for password reset
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expires_at = db.Column(db.DateTime, nullable=True)

    # Timestamp 
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (with other tables)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    # Passwords Methods 

    def set_password(self, password):
        try:
            self.password_hash = generate_password_hash(password)
        except Exception as e:
            raise ValueError(f"Error setting password{str(e)}")
    
    def check_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            return False
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_blocked(self):
        return not self.is_active
    
    # -- OTP Methods -- 
    def set_otp(self, otp_code):
        try:
            from datetime import timedelta
            self.otp_code = otp_code
            self.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        except Exception as e: 
            raise ValueError(f"Error setting OTP: {str(e)}")
    
    def verify_otp(self, otp_code):
        try:
            if self.otp_code is None or self.otp_expires_at is None:
                return False
            if datetime.utcnow() > self.otp_expires_at:
                return False
            return self.otp_code == otp_code
        except Exception as e:
            return False
        
    def clear_otp(self):
        self.otp_code = None
        self.otp_expires_at = None
    
    # -- Profile Methods -- 
    def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def get_profile_completion(self):
        fields = [
            self.first_name,
            self.last_name,
            self.username,
            self.email,
            self.phone
        ]
        filled = sum(1 for field in fields if field)
        return int((filled / len(fields)) * 100)

    # -- Representation --
    def __repr__(self):
        return f'<User {self.username}>'