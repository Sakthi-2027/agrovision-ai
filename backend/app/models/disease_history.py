from datetime import datetime
from app.extensions import db

class DiseaseHistory(db.Model):
    __tablename__ = "disease_history"

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)

    disease_name = db.Column(db.String(100), nullable=False)
    crop_affected = db.Column(db.String(100))
    severity = db.Column(db.String(20))  # "Low" / "Medium" / "High"
    detected_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "disease_name": self.disease_name,
            "crop_affected": self.crop_affected,
            "severity": self.severity,
            "detected_date": self.detected_date.isoformat() if self.detected_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }