from datetime import datetime
from app.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

    # Review Content
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # --- Validation ---

    def validate_rating(self):
        """Ensure rating is between 1 and 5"""
        try:
            if self.rating < 1 or self.rating > 5:
                return False, "Rating must be between 1 and 5"
            return True, "Valid rating"
        except Exception as e:
            return False, f"Rating validation error: {str(e)}"

    # --- Representation ---
    def __repr__(self):
        return f'<Review Room:{self.room_id} Rating:{self.rating}>'