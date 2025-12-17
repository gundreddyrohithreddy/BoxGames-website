from flask import Blueprint, render_template
from app.models.venue import Venue

# THIS NAME MUST MATCH app/__init__.py
player_bp = Blueprint("player", __name__, url_prefix="/player")

@player_bp.route("/dashboard")
def dashboard():
    return render_template("player/dashboard.html")

@player_bp.route("/venues")
def venues():
    venues = Venue.query.all()
    return render_template("player/venues.html", venues=venues)
