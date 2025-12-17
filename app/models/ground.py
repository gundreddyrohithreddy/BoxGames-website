from ..extensions import db

class Ground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
    name = db.Column(db.String(100))
    sport_type = db.Column(db.String(50))
    slot_duration = db.Column(db.Integer)
