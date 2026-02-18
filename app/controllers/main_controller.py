from flask import Blueprint, render_template, request, flash, redirect, url_for, abort

main = Blueprint('main', __name__)

# ==================== HOME ====================
@main.route('/')
def home():
    try:
        return render_template('main/home.html')
    except Exception as e:
        abort(500)

# ==================== ABOUT ====================
@main.route('/about')
def about():
    try:
        return render_template('main/about.html')
    except Exception as e:
        abort(500)

# ==================== CONTACT ====================
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()

            # Validation
            if not all([name, email, subject, message]):
                flash('Please fill in all fields.', 'error')
                return render_template('main/contact.html')

            # TODO: Send email in later phase
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('main.contact'))

        return render_template('main/contact.html')

    except Exception as e:
        abort(500)

# ==================== FAQ ====================
@main.route('/faq')
def faq():
    try:
        return render_template('main/faq.html')
    except Exception as e:
        abort(500)

# ==================== ROOMS (Public Listing) ====================
@main.route('/rooms')
def rooms():
    try:
        return render_template('main/rooms.html')
    except Exception as e:
        abort(500)

# ==================== PRIVACY POLICY ====================
@main.route('/privacy')
def privacy():
    try:
        return render_template('extra/privacy.html')
    except Exception as e:
        abort(500)

# ==================== TERMS OF SERVICE ====================
@main.route('/terms')
def terms():
    try:
        return render_template('extra/terms.html')
    except Exception as e:
        abort(500)