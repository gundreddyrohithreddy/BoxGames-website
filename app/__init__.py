from flask import Flask
from .config import Config
from .extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Import Blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        from .models import roles, users, otps
        db.create_all()

    return app
