from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="farmer")  # "farmer" or "admin"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, plain_password):
        """Hashes and stores the password — never save plain text."""
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """Compares a login attempt against the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def __repr__(self):
        return f"<User {self.email}>"