from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.ml_service import predict_crop

crop_bp = Blueprint("crop", __name__, url_prefix="/api/crop-recommendation")


@crop_bp.route("", methods=["POST"])
@login_required
def recommend_crop():
    data = request.get_json()

    required_fields = ["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"]
    missing = [f for f in required_fields if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        result = predict_crop(
            nitrogen=float(data["nitrogen"]),
            phosphorus=float(data["phosphorus"]),
            potassium=float(data["potassium"]),
            temperature=float(data["temperature"]),
            humidity=float(data["humidity"]),
            ph=float(data["ph"]),
            rainfall=float(data["rainfall"])
        )
    except ValueError:
        return jsonify({"error": "All fields must be numeric"}), 400

    return jsonify(result), 200