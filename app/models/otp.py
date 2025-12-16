from datetime import datetime
from ..extensions import db

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(15), nullable=False)
    otp_code = db.Column(db.String(10), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
