import requests
from flask import current_app
from app.extensions import db
from app.models.market_price import MarketPrice

MARKET_API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


def sync_market_prices(limit=100):
    """
    Pulls fresh data from data.gov.in and replaces our local cache.
    Returns (success: bool, message: str, records_synced: int).
    Never raises — if the external API fails, old data stays untouched.
    """
    params = {
        "api-key": current_app.config["DATA_GOV_API_KEY"],
        "format": "json",
        "limit": limit
    }

    try:
        response = requests.get(MARKET_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])
    except requests.exceptions.RequestException as e:
        return False, f"Sync failed (external API issue): {e}", 0

    if not records:
        return False, "Sync completed but the API returned no records.", 0

    # Clear old data and insert fresh — simple full-replace strategy for this scale
    MarketPrice.query.delete()

    for r in records:
        price = MarketPrice(
            state=r.get("state"),
            district=r.get("district"),
            market=r.get("market"),
            commodity=r.get("commodity"),
            variety=r.get("variety"),
            min_price=safe_float(r.get("min_price")),
            max_price=safe_float(r.get("max_price")),
            modal_price=safe_float(r.get("modal_price")),
            arrival_date=r.get("arrival_date")
        )
        db.session.add(price)

    db.session.commit()
    return True, f"Synced {len(records)} records successfully.", len(records)


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_market_prices(state=None, commodity=None, limit=50):
    """Reads from OUR database — fast and always available, independent of external API uptime."""
    query = MarketPrice.query

    if state:
        query = query.filter(MarketPrice.state.ilike(f"%{state}%"))
    if commodity:
        query = query.filter(MarketPrice.commodity.ilike(f"%{commodity}%"))

    return query.limit(limit).all()