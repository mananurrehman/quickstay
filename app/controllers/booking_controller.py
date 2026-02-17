from flask import Blueprint

booking = Blueprint('booking', __name__, url_prefix='/bookings')

@booking.route('/')
def list():
    return "Bookings page coming soon", 200