import os
import joblib

# Load the model once when this module is first imported — not on every request
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "crop_recommendation_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

_crop_model = None


def get_crop_model():
    """Lazy-loads the model once, reuses it for every request after that."""
    global _crop_model
    if _crop_model is None:
        _crop_model = joblib.load(MODEL_PATH)
    return _crop_model


def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    model = get_crop_model()

    features = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities) * 100

    return {
        "recommended_crop": prediction,
        "confidence": round(confidence, 2)
    }
FERTILIZER_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "fertilizer_recommendation_model.pkl")
FERTILIZER_MODEL_PATH = os.path.abspath(FERTILIZER_MODEL_PATH)

_fertilizer_bundle = None


def get_fertilizer_bundle():
    global _fertilizer_bundle
    if _fertilizer_bundle is None:
        _fertilizer_bundle = joblib.load(FERTILIZER_MODEL_PATH)
    return _fertilizer_bundle


def predict_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorous):
    bundle = get_fertilizer_bundle()
    model = bundle["model"]
    soil_encoder = bundle["soil_encoder"]
    crop_encoder = bundle["crop_encoder"]

    
    try:
        soil_encoded = soil_encoder.transform([soil_type])[0]
    except ValueError:
        return {"error": f"Unknown soil type: '{soil_type}'. Known types: {list(soil_encoder.classes_)}"}

    try:
        crop_encoded = crop_encoder.transform([crop_type])[0]
    except ValueError:
        return {"error": f"Unknown crop type: '{crop_type}'. Known types: {list(crop_encoder.classes_)}"}

    features = [[temperature, humidity, moisture, soil_encoded, crop_encoded, nitrogen, potassium, phosphorous]]

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities) * 100

    return {
        "recommended_fertilizer": prediction,
        "confidence": round(confidence, 2)
    }


def get_fertilizer_options():
    
    bundle = get_fertilizer_bundle()
    return {
        "soil_types": list(bundle["soil_encoder"].classes_),
        "crop_types": list(bundle["crop_encoder"].classes_)
    }