from datetime import datetime
from app.extensions import db

class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    farm_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200))
    size_in_acres = db.Column(db.Float)
    soil_type = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Converts this model to a JSON-friendly dictionary."""
        return {
            "id": self.id,
            "farm_name": self.farm_name,
            "location": self.location,
            "size_in_acres": self.size_in_acres,
            "soil_type": self.soil_type,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Farm {self.farm_name}>"