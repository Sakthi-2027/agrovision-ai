import click
from flask import Flask
from config.config import Config
from app.extensions import db, login_manager, cors
from app.models.user import User 
from app.models.user import User  
from app.models.farm import Farm 
from app.models.crop_history import CropHistory  
from app.models.fertilizer_history import FertilizerHistory 
from app.models.disease_history import DiseaseHistory 
from app.models.notification import Notification  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://localhost:5500", "null"])

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.farm_routes import farm_bp
    app.register_blueprint(farm_bp)

    from app.routes.weather_routes import weather_bp
    app.register_blueprint(weather_bp)

    from app.routes.market_routes import market_bp
    app.register_blueprint(market_bp)

    from app.routes.notification_routes import notification_bp
    app.register_blueprint(notification_bp)
    from app.routes.analytics_routes import analytics_bp
    app.register_blueprint(analytics_bp)
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return {"message": "AgroVision AI backend is running 🌱"}

    @app.cli.command("create-db")
    def create_db():
        db.create_all()
        print("✅ Database tables created successfully.")

    @app.cli.command("make-admin")
    @click.argument("email")
    def make_admin(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"❌ No user found with email: {email}")
            return
        user.role = "admin"
        db.session.commit()
        print(f"✅ {user.full_name} ({email}) is now an admin.")

    return app