import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///boxgames.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
