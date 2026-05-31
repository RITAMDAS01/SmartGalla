from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import auth_bp
from app.auth.forms import LoginForm
from app.models import User

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Admin':
            flash('You do not have permission to access that page.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/staff', methods=['GET', 'POST'])
@login_required
@admin_required
def staff():
    from app.auth.forms import StaffForm
    from app.extensions import db
    
    form = StaffForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.set_password('123456') # Default pass
        db.session.add(user)
        db.session.commit()
        flash('Staff member added successfully.', 'success')
        return redirect(url_for('auth.staff'))
        
    staff_list = User.query.all()
    return render_template('auth/staff.html', staff=staff_list, form=form, title='Staff Management')

@auth_bp.route('/staff/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_staff(id):
    from app.extensions import db
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete yourself!', 'danger')
    elif user.username == 'admin':
        flash('Cannot delete the main admin account.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'Staff member {user.username} deleted.', 'success')
    return redirect(url_for('auth.staff'))
