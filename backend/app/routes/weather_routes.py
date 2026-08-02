from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.weather_service import get_coordinates, get_forecast

weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")


@weather_bp.route("", methods=["GET"])
@login_required
def weather():
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "location query parameter is required"}), 400

    coords = get_coordinates(location)
    if not coords:
        return jsonify({"error": f"Could not find location: {location}"}), 404

    forecast_data = get_forecast(coords["latitude"], coords["longitude"])

    return jsonify({
        "resolved_location": coords["resolved_name"],
        "current": forecast_data["current"],
        "daily": forecast_data["daily"]
    }), 200