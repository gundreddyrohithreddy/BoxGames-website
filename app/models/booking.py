from datetime import datetime
from ..extensions import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey("slot.id"))
    user_id = db.Column(db.Integer)
    status = db.Column(db.String(50), default="CONFIRMED")
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
