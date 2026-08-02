from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models.market_price import MarketPrice
from app.services.market_service import get_market_prices

market_bp = Blueprint("market", __name__, url_prefix="/api/market-prices")


@market_bp.route("", methods=["GET"])
@login_required
def market_prices():
    state = request.args.get("state")
    commodity = request.args.get("commodity")

    records = get_market_prices(state=state, commodity=commodity)

    latest = MarketPrice.query.order_by(MarketPrice.synced_at.desc()).first()
    last_synced = latest.synced_at.isoformat() if latest else None

    return jsonify({
        "count": len(records),
        "last_synced": last_synced,
        "records": [r.to_dict() for r in records]
    }), 200