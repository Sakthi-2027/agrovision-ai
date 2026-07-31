import os

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(os.getcwd(), "instance", "agrovision.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False