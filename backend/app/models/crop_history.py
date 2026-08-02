from datetime import datetime
from app.extensions import db

class CropHistory(db.Model):
    __tablename__ = "crop_history"

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)

    crop_name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(50))
    planting_date = db.Column(db.Date)
    harvest_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "crop_name": self.crop_name,
            "season": self.season,
            "planting_date": self.planting_date.isoformat() if self.planting_date else None,
            "harvest_date": self.harvest_date.isoformat() if self.harvest_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }