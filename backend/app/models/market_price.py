from datetime import datetime
from app.extensions import db

class MarketPrice(db.Model):
    __tablename__ = "market_prices"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    market = db.Column(db.String(150))
    commodity = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    modal_price = db.Column(db.Float)
    arrival_date = db.Column(db.String(20))  # kept as text — source format varies

    synced_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "district": self.district,
            "market": self.market,
            "commodity": self.commodity,
            "variety": self.variety,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "modal_price": self.modal_price,
            "arrival_date": self.arrival_date
        }