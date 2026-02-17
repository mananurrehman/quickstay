from datetime import datetime
from app.extensions import db

class Room(db.Model):
    __tablename__ = 'rooms'
    # ID
    id = db.Column(db.Integer, primary_key=True)

    # Room Info
    name = db.Column(db.String(100), nullable=False)
    #Type =  Standard, Deluxe, Premium, Family
    room_type = db.Column(db.String(20), nullable=False)  
    description = db.Column(db.Text, nullable=True)

    # Pricing & Capacity
    price_per_night = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False, default=2)
    room_size = db.Column(db.String(20), nullable=True)  # e.g., "35 sqm"

    # Amenities (comma seperated values)
    amenities = db.Column(db.Text, nullable=True)  # "WiFi,TV,AC etc"

    # Image
    image = db.Column(db.String(256), nullable=True, default='default_room.jpg')

    # Status
    status = db.Column(db.String(20), default='available', nullable=False)
    # status = available, booked, maintenance

    # Rating
    rating = db.Column(db.Float, default=0.0)

    #TimeStamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    bookings = db.relationship('Booking', backref='room', lazy='dynamic')
    reviews = db.relationship('Review', backref='room', lazy='dynamic')

    # Amenity Methods
    
    def get_amenities_list(self):
        try:
            if self.amenities:
                return [a.strip() for a in self.amenities.split(',')]
            return []
        except Exception as e:
            return []

    def set_amenities_list(self, amenities_list):
        try:
            if amenities_list:
                self.amenities = ','.join(amenities_list)
            else:
                self.amenities = None
        except Exception as e:
            self.amenities = None

    # Status
    def is_available(self):
        return self.status == 'available'

    def is_under_maintenance(self):
        return self.status == 'maintenance'

    # Booking Check
    def has_active_bookings(self):
        try:
            from app.models.bookings import Booking
            active_count = self.bookings.filter(
                Booking.status.in_(['confirmed', 'pending'])
            ).count()
            return active_count > 0
        except Exception as e:
            return False

    def is_available_for_dates(self, check_in, check_out):
        try:
            from app.models.bookings import Booking
            conflicting = self.bookings.filter(
                Booking.status.in_(['confirmed', 'pending']),
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            ).count()
            return conflicting == 0
        except Exception as e:
            return False

    # Rating
    def update_rating(self):
        try:
            from app.models.review import Review
            reviews = self.reviews.all()
            if reviews:
                total = sum(r.rating for r in reviews)
                self.rating = round(total / len(reviews), 1)
            else:
                self.rating = 0.0
        except Exception as e:
            self.rating = 0.0

    # Represenation 
    def __repr__(self):
        return f'<Room {self.name} ({self.room_type})>'