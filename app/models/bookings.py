from datetime import datetime
from app.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

    # Booking Details
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    guests_count = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)

    # Status
    status = db.Column(db.String(20), default='pending', nullable=False)
    # 'pending', 'confirmed', 'cancelled', 'rejected'

    # Admin action
    rejection_reason = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Calculation Methods ---
    def calculate_nights(self):
        try:
            delta = self.check_out_date - self.check_in_date
            return delta.days
        except Exception as e:
            return 0

    def calculate_total_price(self, price_per_night):
        try:
            nights = self.calculate_nights()
            self.total_price = nights * price_per_night
            return self.total_price
        except Exception as e:
            self.total_price = 0
            return 0

    # --- Validation Methods ---
    def validate_dates(self):
        try:
            today = datetime.utcnow().date()

            # Rule 1: Cannot book past dates
            if self.check_in_date < today:
                return False, "Check-in date cannot be in the past"

            # Rule 2: Check-out must be after check-in
            if self.check_out_date <= self.check_in_date:
                return False, "Check-out date must be after check-in date"

            # Rule 3: Minimum 1-night stay
            if self.calculate_nights() < 1:
                return False, "Minimum 1-night stay required"

            return True, "Dates are valid"

        except Exception as e:
            return False, f"Date validation error: {str(e)}"

    # --- Status Methods ---
    def is_upcoming(self):
        try:
            today = datetime.utcnow().date()
            return self.status in ['confirmed', 'pending'] and self.check_in_date >= today
        except Exception as e:
            return False

    def is_past(self):
        try:
            today = datetime.utcnow().date()
            return self.check_out_date < today
        except Exception as e:
            return False

    def is_cancelled(self):
        return self.status == 'cancelled'

    def can_cancel(self):
        try:
            today = datetime.utcnow().date()
            return (
                self.status in ['confirmed', 'pending']
                and self.check_in_date > today
            )
        except Exception as e:
            return False

    # --- Action Methods ---
    def cancel(self):
        try:
            if not self.can_cancel():
                return False, "This booking cannot be cancelled"
            self.status = 'cancelled'
            return True, "Booking cancelled successfully"
        except Exception as e:
            return False, f"Error cancelling booking: {str(e)}"

    def approve(self):
        try:
            if self.status != 'pending':
                return False, "Only pending bookings can be approved"
            self.status = 'confirmed'
            return True, "Booking approved successfully"
        except Exception as e:
            return False, f"Error approving booking: {str(e)}"

    def reject(self, reason=None):
        try:
            if self.status != 'pending':
                return False, "Only pending bookings can be rejected"
            self.status = 'rejected'
            self.rejection_reason = reason
            return True, "Booking rejected"
        except Exception as e:
            return False, f"Error rejecting booking: {str(e)}"

    # --- Representation ---
    def __repr__(self):
        return f'<Booking {self.id} - Room {self.room_id} ({self.status})>'