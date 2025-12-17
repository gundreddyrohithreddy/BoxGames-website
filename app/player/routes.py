from flask import Blueprint, render_template
from app.models.venue import Venue
from datetime import datetime, timedelta
# THIS NAME MUST MATCH app/__init__.py
player_bp = Blueprint("player", __name__, url_prefix="/player")

@player_bp.route("/dashboard")
def dashboard():
    return render_template("player/dashboard.html")

@player_bp.route("/venues")
def venues():
    venues = Venue.query.all()
    return render_template("player/venues.html", venues=venues)

@player_bp.route("/book/<int:slot_id>", methods=["POST"])
@login_required("player")
def book_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)

    if slot.is_booked:
        return "Slot already booked", 400

    booking = Booking(
        slot_id=slot.id,
        user_id=session["user_id"]
    )

    slot.is_booked = True
    db.session.add(booking)
    db.session.commit()

    return redirect("/player/bookings")

@player_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required("player")
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    slot = Slot.query.get(booking.slot_id)

    slot_time = datetime.strptime(
        f"{slot.slot_date} {slot.start_time}", "%Y-%m-%d %H:%M"
    )

    if datetime.now() > slot_time - timedelta(hours=1):
        return "Cancellation window closed", 400

    slot.is_booked = False
    db.session.delete(booking)
    db.session.commit()

    return redirect("/player/bookings")
