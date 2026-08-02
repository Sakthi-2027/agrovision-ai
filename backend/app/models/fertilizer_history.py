from datetime import datetime
from app.extensions import db

class FertilizerHistory(db.Model):
    __tablename__ = "fertilizer_history"

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)

    fertilizer_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))
    application_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "farm_id": self.farm_id,
            "fertilizer_name": self.fertilizer_name,
            "quantity": self.quantity,
            "unit": self.unit,
            "application_date": self.application_date.isoformat() if self.application_date else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }