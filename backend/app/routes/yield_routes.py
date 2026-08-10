from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.ml_service import predict_yield, get_yield_options

yield_bp = Blueprint("yield_prediction", __name__, url_prefix="/api/yield-prediction")


@yield_bp.route("/options", methods=["GET"])
@login_required
def yield_options():
    return jsonify(get_yield_options()), 200


@yield_bp.route("", methods=["POST"])
@login_required
def predict_yield_route():
    data = request.get_json()

    required = ["area", "item", "year", "rainfall", "pesticides", "avg_temp"]
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        result = predict_yield(
            area=data["area"],
            item=data["item"],
            year=int(data["year"]),
            rainfall=float(data["rainfall"]),
            pesticides=float(data["pesticides"]),
            avg_temp=float(data["avg_temp"])
        )
    except ValueError:
        return jsonify({"error": "Numeric fields must be valid numbers"}), 400

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200