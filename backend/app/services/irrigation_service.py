from app.services.weather_service import get_coordinates, get_forecast

# Crop water requirements (mm/day) — standard agronomic values
CROP_WATER_NEEDS = {
    "Rice": 6.0,
    "Wheat": 4.5,
    "Maize": 5.0,
    "Cotton": 5.5,
    "Sugarcane": 7.0,
    "Potato": 4.0,
    "Tomato": 4.5,
    "Onion": 3.5,
    "Soybean": 4.0,
    "Groundnut": 3.5,
    "Barley": 3.5,
    "Millets": 3.0,
    "Pulses": 3.0,
    "Vegetables": 4.0,
    "Other": 4.0
}

# Soil moisture thresholds (%) below which irrigation is needed
SOIL_MOISTURE_THRESHOLDS = {
    "Sandy": 25,
    "Loamy": 35,
    "Black": 40,
    "Red": 30,
    "Clayey": 45
}


def get_irrigation_recommendation(crop_type, soil_type, current_moisture, location):
    """
    Returns an irrigation recommendation based on:
    - current soil moisture vs threshold for that soil type
    - upcoming rainfall from the real weather forecast
    - crop's daily water need
    """
    result = {
        "crop_type": crop_type,
        "soil_type": soil_type,
        "current_moisture": current_moisture,
        "location": location,
        "weather_used": False,
        "upcoming_rain_mm": 0,
        "recommendation": None,
        "reason": None
    }

    # Get soil moisture threshold
    threshold = SOIL_MOISTURE_THRESHOLDS.get(soil_type, 35)
    crop_need = CROP_WATER_NEEDS.get(crop_type, 4.0)

    # Try to get real weather forecast
    try:
        coords = get_coordinates(location)
        if coords:
            forecast = get_forecast(coords["latitude"], coords["longitude"])
            daily = forecast.get("daily", {})
            rain_next_2_days = sum(daily.get("precipitation_sum", [0, 0])[:2])
            result["weather_used"] = True
            result["upcoming_rain_mm"] = round(rain_next_2_days, 1)
            result["resolved_location"] = coords["resolved_name"]
        else:
            rain_next_2_days = 0
    except Exception:
        rain_next_2_days = 0

    # Decision logic
    if rain_next_2_days >= crop_need * 2:
        result["recommendation"] = "Skip — rain expected"
        result["reason"] = (
            f"{result['upcoming_rain_mm']}mm of rain expected in the next 2 days, "
            f"which meets {crop_type}'s water needs. No irrigation required."
        )
    elif current_moisture < threshold:
        if rain_next_2_days > 0:
            result["recommendation"] = "Irrigate lightly"
            result["reason"] = (
                f"Soil moisture ({current_moisture}%) is below the {soil_type} soil threshold ({threshold}%). "
                f"Some rain expected ({result['upcoming_rain_mm']}mm), so light irrigation is sufficient."
            )
        else:
            result["recommendation"] = "Irrigate now"
            result["reason"] = (
                f"Soil moisture ({current_moisture}%) is below the {soil_type} soil threshold ({threshold}%) "
                f"and no significant rainfall is expected. Irrigate based on {crop_type}'s "
                f"water need of {crop_need}mm/day."
            )
    else:
        result["recommendation"] = "No irrigation needed"
        result["reason"] = (
            f"Soil moisture ({current_moisture}%) is above the threshold for {soil_type} soil ({threshold}%). "
            f"Monitor and reassess in 1-2 days."
        )

    return result