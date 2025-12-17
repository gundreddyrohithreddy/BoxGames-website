from flask import Blueprint, render_template
from app.models.venue import Venue

# IMPORTANT: name must be owner_bp
owner_bp = Blueprint("owner", __name__, url_prefix="/owner")

@owner_bp.route("/dashboard")
def dashboard():
    return render_template("owner/dashboard.html")

@owner_bp.route("/venues")
def venues():
    venues = Venue.query.all()
    return render_template("owner/venues.html", venues=venues)
