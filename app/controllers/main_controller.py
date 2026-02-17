from flask import Blueprint, render_template, request, flash, redirect, url_for

main = Blueprint('main', __name__)

# ==================== HOME ====================
@main.route('/')
def home():
    try:
        return render_template('main/home.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')

# ==================== ABOUT ====================
@main.route('/about')
def about():
    try:
        return render_template('main/about.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')

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

            # Todo : Send email in later phase
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('main.contact'))

        return render_template('main/contact.html')

    except Exception as e:
        flash('Something went wrong. Please try again.', 'error')
        return render_template('main/contact.html')

# ==================== FAQ ====================
@main.route('/faq')
def faq():
    try:
        return render_template('main/faq.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')

# ==================== ROOMS (Public Listing) ====================
@main.route('/rooms')
def rooms():
    try:
        return render_template('main/rooms.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')

# ==================== PRIVACY POLICY ====================
@main.route('/privacy')
def privacy():
    try:
        return render_template('extra/privacy.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')

# ==================== TERMS OF SERVICE ====================
@main.route('/terms')
def terms():
    try:
        return render_template('extra/terms.html')
    except Exception as e:
        flash('Something went wrong loading the page.', 'error')
        return render_template('main/home.html')