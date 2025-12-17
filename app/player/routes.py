from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from app.models import Venue, Ground, Slot, Booking
from app import db
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import or_

from flask import Blueprint

player = Blueprint(
    'player',
    __name__,
    template_folder='templates'
)

@player.route('/')
@player.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'player':
        return abort(403)
    venues = Venue.query.all()
    return render_template('player/dashboard.html', venues=venues)

@player.route('/venues')
@login_required
def venues():
    if current_user.role != 'player':
        return abort(403)
    search = request.args.get('search')
    date = request.args.get('date')
    venues_query = Venue.query
    if search:
        venues_query = venues_query.filter(or_(Venue.name.contains(search), Venue.location.contains(search)))
    venues = venues_query.all()
    return render_template('player/venues.html', venues=venues, date=date, search=search)

@player.route('/venues/<int:venue_id>')
@login_required
def venue_detail(venue_id):
    if current_user.role != 'player':
        return abort(403)
    venue = Venue.query.get_or_404(venue_id)
    date = request.args.get('date')
    grounds = Ground.query.filter_by(venue_id=venue.id).all()
    # Gather available slots per ground
    available_slots = {}
    for ground in grounds:
        slots_query = Slot.query.filter_by(ground_id=ground.id, is_booked=False)
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                slots = [slot for slot in slots_query if slot.start_time.date() == date_obj]
            except ValueError:
                slots = slots_query.all()
        else:
            slots = slots_query.all()
        available_slots[ground] = slots
    return render_template('player/venue_detail.html', venue=venue, grounds=grounds, available_slots=available_slots, date=date)

@player.route('/book/<int:slot_id>')
@login_required
def book_slot(slot_id):
    if current_user.role != 'player':
        return abort(403)
    slot = Slot.query.get_or_404(slot_id)
    if slot.is_booked:
        flash('Slot is already booked.', 'warning')
        return redirect(url_for('player.venues'))
    slot.is_booked = True
    booking = Booking(slot_id=slot.id, user_id=current_user.id, timestamp=datetime.utcnow())
    db.session.add(booking)
    db.session.commit()
    flash('Slot booked successfully!', 'success')
    return redirect(url_for('player.bookings'))

# @player.route('/bookings')
# @login_required
# def bookings():
#     if current_user.role != 'player':
#         return abort(403)
#     bookings = Booking.query.filter_by(user_id=current_user.id).all()
#     return render_template('player/bookings.html', bookings=bookings)

@player.route('/bookings')
@login_required
def bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('player/bookings.html', bookings=bookings)
