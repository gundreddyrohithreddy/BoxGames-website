from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="player")

    def __repr__(self):
        return f"<User {self.email}>"


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Venue {self.name}>"


class Ground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))

    def __repr__(self):
        return f"<Ground {self.name}>"


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ground_id = db.Column(db.Integer, db.ForeignKey("ground.id"))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Slot {self.start_time} - {self.end_time}>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    slot_id = db.Column(db.Integer, db.ForeignKey("slot.id"))
