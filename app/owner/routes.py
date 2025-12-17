from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app.models import Venue, Ground, Slot
from app import db
from flask_login import current_user, login_required
from datetime import datetime

owner = Blueprint('owner', __name__)

@owner.route('/')
@owner.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'owner':
        return abort(403)
    venues = Venue.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/dashboard.html', venues=venues)

@owner.route('/venues')
@login_required
def venues():
    if current_user.role != 'owner':
        return abort(403)
    venues = Venue.query.filter_by(owner_id=current_user.id).all()
    return render_template('owner/venues.html', venues=venues)

@owner.route('/venues/create', methods=['GET', 'POST'])
@login_required
def create_venue():
    if current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        venue = Venue(name=name, location=location, owner_id=current_user.id)
        db.session.add(venue)
        db.session.commit()
        flash('Venue created successfully.', 'success')
        return redirect(url_for('owner.venues'))
    return render_template('owner/create_venue.html')

@owner.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        venue.name = request.form.get('name')
        venue.location = request.form.get('location')
        db.session.commit()
        flash('Venue updated successfully.', 'success')
        return redirect(url_for('owner.venues'))
    return render_template('owner/edit_venue.html', venue=venue)

@owner.route('/venues/<int:venue_id>/delete', methods=['POST'])
@login_required
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted.', 'info')
    return redirect(url_for('owner.venues'))

@owner.route('/venues/<int:venue_id>/grounds')
@login_required
def grounds(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    grounds = Ground.query.filter_by(venue_id=venue.id).all()
    return render_template('owner/grounds.html', venue=venue, grounds=grounds)

@owner.route('/venues/<int:venue_id>/grounds/create', methods=['GET', 'POST'])
@login_required
def create_ground(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        name = request.form.get('name')
        ground = Ground(name=name, venue_id=venue.id)
        db.session.add(ground)
        db.session.commit()
        flash('Ground created successfully.', 'success')
        return redirect(url_for('owner.grounds', venue_id=venue.id))
    return render_template('owner/create_ground.html', venue=venue)

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ground(venue_id, ground_id):
    ground = Ground.query.get_or_404(ground_id)
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        ground.name = request.form.get('name')
        db.session.commit()
        flash('Ground updated successfully.', 'success')
        return redirect(url_for('owner.grounds', venue_id=venue.id))
    return render_template('owner/edit_ground.html', venue=venue, ground=ground)

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/delete', methods=['POST'])
@login_required
def delete_ground(venue_id, ground_id):
    ground = Ground.query.get_or_404(ground_id)
    venue = Venue.query.get_or_404(venue_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    db.session.delete(ground)
    db.session.commit()
    flash('Ground deleted.', 'info')
    return redirect(url_for('owner.grounds', venue_id=venue_id))

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/slots')
@login_required
def slots(venue_id, ground_id):
    venue = Venue.query.get_or_404(venue_id)
    ground = Ground.query.get_or_404(ground_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    slots = Slot.query.filter_by(ground_id=ground.id).all()
    return render_template('owner/slots.html', venue=venue, ground=ground, slots=slots)

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/slots/create', methods=['GET', 'POST'])
@login_required
def create_slot(venue_id, ground_id):
    venue = Venue.query.get_or_404(venue_id)
    ground = Ground.query.get_or_404(ground_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            flash('Invalid date/time format', 'danger')
            return redirect(url_for('owner.slots', venue_id=venue.id, ground_id=ground.id))
        slot = Slot(ground_id=ground.id, start_time=start_time, end_time=end_time)
        db.session.add(slot)
        db.session.commit()
        flash('Slot created successfully.', 'success')
        return redirect(url_for('owner.slots', venue_id=venue.id, ground_id=ground.id))
    return render_template('owner/create_slot.html', venue=venue, ground=ground)

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/slots/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_slot(venue_id, ground_id, slot_id):
    venue = Venue.query.get_or_404(venue_id)
    ground = Ground.query.get_or_404(ground_id)
    slot = Slot.query.get_or_404(slot_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    db.session.delete(slot)
    db.session.commit()
    flash('Slot deleted.', 'info')
    return redirect(url_for('owner.slots', venue_id=venue.id, ground_id=ground.id))

@owner.route('/venues/<int:venue_id>/grounds/<int:ground_id>/slots/<int:slot_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_slot(venue_id, ground_id, slot_id):
    venue = Venue.query.get_or_404(venue_id)
    ground = Ground.query.get_or_404(ground_id)
    slot = Slot.query.get_or_404(slot_id)
    if venue.owner_id != current_user.id or current_user.role != 'owner':
        return abort(403)
    if request.method == 'POST':
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        try:
            slot.start_time = datetime.fromisoformat(start_time_str)
            slot.end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            flash('Invalid date/time format', 'danger')
            return redirect(url_for('owner.slots', venue_id=venue.id, ground_id=ground.id))
        db.session.commit()
        flash('Slot updated successfully.', 'success')
        return redirect(url_for('owner.slots', venue_id=venue.id, ground_id=ground.id))
    return render_template('owner/edit_slot.html', venue=venue, ground=ground, slot=slot)
