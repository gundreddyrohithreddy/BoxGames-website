from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app.models import User, Venue
from app import db, bcrypt
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return abort(403)
    users = User.query.all()
    venues = Venue.query.all()
    return render_template('admin/dashboard.html', users=users, venues=venues)

@admin.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        return abort(403)
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return abort(403)
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        role = request.form.get('role')
        if role in ['player', 'owner', 'admin']:
            user.role = role
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', user=user)

@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'info')
    return redirect(url_for('admin.users'))

@admin.route('/venues')
@login_required
def venues():
    if current_user.role != 'admin':
        return abort(403)
    venues = Venue.query.all()
    return render_template('admin/venues.html', venues=venues)

@admin.route('/venues/create', methods=['GET', 'POST'])
@login_required
def create_venue():
    if current_user.role != 'admin':
        return abort(403)
    owners = User.query.filter_by(role='owner').all()
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        owner_id = request.form.get('owner_id')
        venue = Venue(name=name, location=location, owner_id=owner_id)
        db.session.add(venue)
        db.session.commit()
        flash('Venue created successfully.', 'success')
        return redirect(url_for('admin.venues'))
    return render_template('admin/create_venue.html', owners=owners)

@admin.route('/venues/edit/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def edit_venue(venue_id):
    if current_user.role != 'admin':
        return abort(403)
    venue = Venue.query.get_or_404(venue_id)
    owners = User.query.filter_by(role='owner').all()
    if request.method == 'POST':
        venue.name = request.form.get('name')
        venue.location = request.form.get('location')
        venue.owner_id = request.form.get('owner_id')
        db.session.commit()
        flash('Venue updated successfully.', 'success')
        return redirect(url_for('admin.venues'))
    return render_template('admin/edit_venue.html', venue=venue, owners=owners)

@admin.route('/venues/delete/<int:venue_id>', methods=['POST'])
@login_required
def delete_venue(venue_id):
    if current_user.role != 'admin':
        return abort(403)
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted.', 'info')
    return redirect(url_for('admin.venues'))
