from flask import Flask
from config.config import Config
from app.extensions import db, login_manager, cors
from app.models.user import User  # noqa: F401

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    # Tells Flask-Login how to load a user from the ID stored in the session cookie
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register our auth routes
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return {"message": "AgroVision AI backend is running 🌱"}

    @app.cli.command("create-db")
    def create_db():
        db.create_all()
        print("✅ Database tables created successfully.")

    return app