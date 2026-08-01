from flask import Flask
from config.config import Config
from app.extensions import db, login_manager, cors
from app.models.user import User  # noqa: F401  (import registers the table with SQLAlchemy)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    @app.route("/")
    def home():
        return {"message": "AgroVision AI backend is running 🌱"}

    # Custom CLI command: lets us run `flask create-db` in the terminal
    @app.cli.command("create-db")
    def create_db():
        """Creates all database tables based on our models."""
        db.create_all()
        print("✅ Database tables created successfully.")

    return app