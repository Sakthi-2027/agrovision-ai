import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from app.extensions import db
from app.models.market_price import MarketPrice
from datetime import date

SAMPLE_PRICES = [
    {"commodity": "Rice", "variety": "Common", "market": "Koyambedu", "district": "Chennai", "state": "Tamil Nadu", "min_price": 2100, "max_price": 2400, "modal_price": 2250},
    {"commodity": "Wheat", "variety": "Sharbati", "market": "Azadpur", "district": "Delhi", "state": "Delhi", "min_price": 2200, "max_price": 2600, "modal_price": 2400},
    {"commodity": "Maize", "variety": "Hybrid", "market": "Gulbarga", "district": "Gulbarga", "state": "Karnataka", "min_price": 1800, "max_price": 2100, "modal_price": 1950},
    {"commodity": "Onion", "variety": "Local", "market": "Lasalgaon", "district": "Nashik", "state": "Maharashtra", "min_price": 800, "max_price": 1200, "modal_price": 1000},
    {"commodity": "Tomato", "variety": "Local", "market": "Koyambedu", "district": "Chennai", "state": "Tamil Nadu", "min_price": 1200, "max_price": 2000, "modal_price": 1600},
    {"commodity": "Potato", "variety": "Jyoti", "market": "Agra", "district": "Agra", "state": "Uttar Pradesh", "min_price": 900, "max_price": 1200, "modal_price": 1050},
    {"commodity": "Cotton", "variety": "Long Staple", "market": "Rajkot", "district": "Rajkot", "state": "Gujarat", "min_price": 6000, "max_price": 6800, "modal_price": 6400},
    {"commodity": "Soybean", "variety": "Yellow", "market": "Indore", "district": "Indore", "state": "Madhya Pradesh", "min_price": 4200, "max_price": 4800, "modal_price": 4500},
    {"commodity": "Groundnut", "variety": "Bold", "market": "Rajkot", "district": "Rajkot", "state": "Gujarat", "min_price": 5500, "max_price": 6200, "modal_price": 5800},
    {"commodity": "Banana", "variety": "Robusta", "market": "Kolhapur", "district": "Kolhapur", "state": "Maharashtra", "min_price": 1400, "max_price": 1800, "modal_price": 1600},
    {"commodity": "Sugarcane", "variety": "Co-86032", "market": "Coimbatore", "district": "Coimbatore", "state": "Tamil Nadu", "min_price": 280, "max_price": 320, "modal_price": 300},
    {"commodity": "Turmeric", "variety": "Finger", "market": "Erode", "district": "Erode", "state": "Tamil Nadu", "min_price": 7000, "max_price": 8500, "modal_price": 7800},
    {"commodity": "Chilli", "variety": "Teja", "market": "Guntur", "district": "Guntur", "state": "Andhra Pradesh", "min_price": 8000, "max_price": 12000, "modal_price": 10000},
    {"commodity": "Garlic", "variety": "Local", "market": "Neemuch", "district": "Neemuch", "state": "Madhya Pradesh", "min_price": 3000, "max_price": 5000, "modal_price": 4000},
    {"commodity": "Mango", "variety": "Alphonso", "market": "Ratnagiri", "district": "Ratnagiri", "state": "Maharashtra", "min_price": 8000, "max_price": 15000, "modal_price": 12000},
]

def seed():
    app = create_app()
    with app.app_context():
        MarketPrice.query.delete()

        today = date.today().isoformat()
        for item in SAMPLE_PRICES:
            price = MarketPrice(
                state=item["state"],
                district=item["district"],
                market=f"{item['market']} ⚠️ Demo",  # honest label
                commodity=item["commodity"],
                variety=item["variety"],
                min_price=item["min_price"],
                max_price=item["max_price"],
                modal_price=item["modal_price"],
                arrival_date=f"{today} (sample)"
            )
            db.session.add(price)

        db.session.commit()
        print(f"✅ Seeded {len(SAMPLE_PRICES)} sample market price records.")
        print("⚠️  These are sample/demo prices, not live data.")

if __name__ == "__main__":
    seed()