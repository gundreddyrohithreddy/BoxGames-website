from flask import Blueprint, render_template, request, redirect, session
from datetime import datetime, timedelta
import random

from ..extensions import db, bcrypt
from ..models.user import User, Role
from ..models.otp import OTP

auth_bp = Blueprint("auth_bp", __name__)

def generate_otp():
    return f"{random.randint(1000, 9999)}"

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]

        if password != confirm_password:
            return "Passwords do not match!"

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=hashed_pwd,
            role_id=1  # default role player
        )
        db.session.add(user)
        db.session.commit()

        otp_code = generate_otp()
        otp = OTP(
            user_phone=phone,
            otp_code=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        db.session.add(otp)
        db.session.commit()

        return redirect("/verify-otp")

    return render_template("auth/register.html")

@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        phone = request.form["phone"]
        otp_code = request.form["otp_code"]

        record = OTP.query.filter_by(user_phone=phone, otp_code=otp_code, is_used=False).first()
        if record and record.expires_at > datetime.utcnow():
            user = User.query.filter_by(phone=phone).first()
            user.is_verified = True
            record.is_used = True
            db.session.commit()
            return redirect("/login")
        return "Invalid/expired OTP"
    return render_template("auth/verify_otp.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        credential = request.form["email_or_phone"]
        password = request.form["password"]
        user = User.query.filter((User.email==credential)|(User.phone==credential)).first()
        if user and bcrypt.check_password_hash(user.password_hash, password) and user.is_verified:
            session["user_id"] = user.id
            return "Logged in successfully!"
        return "Invalid credentials or unverified!"
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
