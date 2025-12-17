from ..extensions import db

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ground_id = db.Column(db.Integer, db.ForeignKey("ground.id"))
    slot_date = db.Column(db.String(10))
    start_time = db.Column(db.String(5))
    end_time = db.Column(db.String(5))
    price = db.Column(db.Float)
    is_booked = db.Column(db.Boolean, default=False)
