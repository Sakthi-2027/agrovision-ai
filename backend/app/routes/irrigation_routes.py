from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.irrigation_service import get_irrigation_recommendation, CROP_WATER_NEEDS, SOIL_MOISTURE_THRESHOLDS

irrigation_bp = Blueprint("irrigation", __name__, url_prefix="/api/irrigation")


@irrigation_bp.route("/options", methods=["GET"])
@login_required
def irrigation_options():
    return jsonify({
        "crop_types": sorted(list(CROP_WATER_NEEDS.keys())),
        "soil_types": sorted(list(SOIL_MOISTURE_THRESHOLDS.keys()))
    }), 200


@irrigation_bp.route("", methods=["POST"])
@login_required
def recommend_irrigation():
    data = request.get_json()

    required = ["crop_type", "soil_type", "current_moisture", "location"]
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        current_moisture = float(data["current_moisture"])
        if not 0 <= current_moisture <= 100:
            return jsonify({"error": "current_moisture must be between 0 and 100"}), 400
    except ValueError:
        return jsonify({"error": "current_moisture must be a number"}), 400

    result = get_irrigation_recommendation(
        crop_type=data["crop_type"],
        soil_type=data["soil_type"],
        current_moisture=current_moisture,
        location=data["location"]
    )

    return jsonify(result), 200