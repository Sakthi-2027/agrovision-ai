from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.market_service import get_market_prices

market_bp = Blueprint("market", __name__, url_prefix="/api/market-prices")


@market_bp.route("", methods=["GET"])
@login_required
def market_prices():
    state = request.args.get("state")
    commodity = request.args.get("commodity")

    records = get_market_prices(state=state, commodity=commodity)
    return jsonify({"count": len(records), "records": records}), 200