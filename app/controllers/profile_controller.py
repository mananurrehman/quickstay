from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from app.extensions import db

profile = Blueprint('profile', __name__, url_prefix='/profile')


# Route 1: View Profile Dashboard

@profile.route('/')
@login_required
def view():
    try:
        return render_template('profile/view.html')
    except Exception as e:
        print(f"Error in profile view: {str(e)}")
        abort(500)


# Route 2: Edit Profile

@profile.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    try:
        if request.method == 'POST':
            # Get form data
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone = request.form.get('phone', '').strip()

            # Validation
            errors = []

            # First name validation
            if not first_name:
                errors.append('First name is required.')
            elif len(first_name) < 3:
                errors.append('First name must be at least 3 characters.')
            elif len(first_name) > 50:
                errors.append('First name must not exceed 50 characters.')

            # Last name validation 
            if last_name and len(last_name) > 60:
                errors.append('Last name must not exceed 60 characters.')

            # Phone validation 
            if phone:
                import re
                if not re.match(r'^[+]?[\d\s\-()]{7,20}$', phone):
                    errors.append('Please enter a valid phone number.')

            # If there are errors, flash them and return
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('profile/edit.html')

            # Update user profile
            try:
                current_user.first_name = first_name
                current_user.last_name = last_name if last_name else None
                current_user.phone = phone if phone else None

                db.session.commit()

                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile.view'))

            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your profile. Please try again.', 'danger')
                print(f"Profile update error: {str(e)}")
                return render_template('profile/edit.html')

        # GET request - show edit form
        return render_template('profile/edit.html')

    except Exception as e:
        print(f"Error in profile edit: {str(e)}")
        abort(500)


# Route 3: Change Password

@profile.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    try:
        if request.method == 'POST':
            # Get form data
            current_password = request.form.get('current_password', '').strip()
            new_password = request.form.get('new_password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()

            errors = []

            if not current_password:
                errors.append('Current password is required.')
            elif not current_user.check_password(current_password):
                errors.append('Current password is incorrect.')

            # New password validation
            if not new_password:
                errors.append('New password is required.')
            elif len(new_password) < 8:
                errors.append('New password must be at least 8 characters.')
            elif not any(c.isupper() for c in new_password):
                errors.append('New password must contain at least one uppercase letter.')
            elif not any(c.islower() for c in new_password):
                errors.append('New password must contain at least one lowercase letter.')
            elif not any(c.isdigit() for c in new_password):
                errors.append('New password must contain at least one number.')
            elif not any(c in '!@#$%^&*(),.?":{}|<>' for c in new_password):
                errors.append('New password must contain at least one special character.')

            # Check new password is different from current
            if current_password and new_password and current_password == new_password:
                errors.append('New password must be different from your current password.')

            # Confirm password check
            if not confirm_password:
                errors.append('Please confirm your new password.')
            elif new_password != confirm_password:
                errors.append('New passwords do not match.')

            # If there are errors, flash them and return
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('profile/change_password.html')

            # Update password
            try:
                current_user.set_password(new_password)
                db.session.commit()

                flash('Password changed successfully!', 'success')
                return redirect(url_for('profile.view'))

            except Exception as e:
                db.session.rollback()
                flash('An error occurred while changing your password. Please try again.', 'danger')
                print(f"Password change error: {str(e)}")
                return render_template('profile/change_password.html')

        # GET request - show change password form
        return render_template('profile/change_password.html')

    except Exception as e:
        print(f"Error in change password: {str(e)}")
        abort(500)


# Route 4: Delete Account

@profile.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    try:
        password = request.form.get('password', '').strip()

        # Verify password before deletion
        if not password:
            flash('Password is required to delete your account.', 'danger')
            return redirect(url_for('profile.view'))

        if not current_user.check_password(password):
            flash('Incorrect password. Account deletion failed.', 'danger')
            return redirect(url_for('profile.view'))

        try:
            # Soft delete - deactivate account instead of hard delete
            current_user.is_active = False
            db.session.commit()

            # Log out the user
            from flask_login import logout_user
            logout_user()

            flash('Your account has been deactivated. Contact support to reactivate.', 'info')
            return redirect(url_for('main.home'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting your account. Please try again.', 'danger')
            print(f"Account deletion error: {str(e)}")
            return redirect(url_for('profile.view'))

    except Exception as e:
        print(f"Error in delete account: {str(e)}")
        abort(500)


# Route 5: Export User Data

@profile.route('/export-data')
@login_required
def export_data():
    try:
        user_data = {
            'personal_info': {
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'username': current_user.username,
                'email': current_user.email,
                'phone': current_user.phone
            },
            'account_info': {
                'role': current_user.role,
                'is_active': current_user.is_active,
                'member_since': current_user.create_at.strftime('%Y-%m-%d %H:%M:%S') if current_user.create_at else None,
                'last_updated': current_user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if current_user.updated_at else None
            }
        }

        response = jsonify(user_data)
        response.headers['Content-Disposition'] = f'attachment; filename={current_user.username}_data.json'
        response.headers['Content-Type'] = 'application/json'
        return response

    except Exception as e:
        print(f"Error in export data: {str(e)}")
        flash('An error occurred while exporting your data.', 'danger')
        return redirect(url_for('profile.view'))