from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.ml_service import predict_fertilizer, get_fertilizer_options

fertilizer_bp = Blueprint("fertilizer", __name__, url_prefix="/api/fertilizer-recommendation")


@fertilizer_bp.route("/options", methods=["GET"])
@login_required
def fertilizer_options():
    return jsonify(get_fertilizer_options()), 200


@fertilizer_bp.route("", methods=["POST"])
@login_required
def recommend_fertilizer():
    data = request.get_json()

    required_fields = ["temperature", "humidity", "moisture", "soil_type", "crop_type", "nitrogen", "potassium", "phosphorous"]
    missing = [f for f in required_fields if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        result = predict_fertilizer(
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            moisture=float(data["moisture"]),
            soil_type=data["soil_type"],
            crop_type=data["crop_type"],
            nitrogen=float(data["nitrogen"]),
            potassium=float(data["potassium"]),
            phosphorous=float(data["phosphorous"])
        )
    except ValueError:
        return jsonify({"error": "Numeric fields must be valid numbers"}), 400

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200