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