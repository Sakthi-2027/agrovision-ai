from flask import Flask
from config.config import Config
from app.extensions import db, login_manager, cors

def create_app():
    """
    Application Factory: builds and configures the Flask app.
    Called from run.py to start the server.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connect our extensions to this specific app instance
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    # A simple test route to confirm the server works
    @app.route("/")
    def home():
        return {"message": "AgroVision AI backend is running 🌱"}

    return app