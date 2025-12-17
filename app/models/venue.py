from ..extensions import db

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
