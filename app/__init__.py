from flask import Flask
from .config import Config
from .extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .player.routes import player_bp
    from .owner.routes import owner_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(owner_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
