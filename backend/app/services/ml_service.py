import os
import joblib


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
YIELD_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "yield_prediction_model.pkl")
YIELD_MODEL_PATH = os.path.abspath(YIELD_MODEL_PATH)

_yield_bundle = None


def get_yield_bundle():
    global _yield_bundle
    if _yield_bundle is None:
        _yield_bundle = joblib.load(YIELD_MODEL_PATH)
    return _yield_bundle


def predict_yield(area, item, year, rainfall, pesticides, avg_temp):
    bundle = get_yield_bundle()
    model = bundle["model"]
    area_encoder = bundle["area_encoder"]
    item_encoder = bundle["item_encoder"]

    try:
        area_encoded = area_encoder.transform([area])[0]
    except ValueError:
        return {"error": f"Unknown area: '{area}'. Known areas: {list(area_encoder.classes_)}"}

    try:
        item_encoded = item_encoder.transform([item])[0]
    except ValueError:
        return {"error": f"Unknown crop: '{item}'. Known crops: {list(item_encoder.classes_)}"}

    features = [[area_encoded, item_encoded, year, rainfall, pesticides, avg_temp]]
    prediction = model.predict(features)[0]

    return {"predicted_yield_hg_per_ha": round(float(prediction), 2)}


def get_yield_options():
    bundle = get_yield_bundle()
    return {
        "areas": sorted(list(bundle["area_encoder"].classes_)),
        "crops": sorted(list(bundle["item_encoder"].classes_))
    }

import json
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np

PEST_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "pest_prediction_model.keras")
PEST_MODEL_PATH = os.path.abspath(PEST_MODEL_PATH)

PEST_LABELS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "pest_class_labels.json")
PEST_LABELS_PATH = os.path.abspath(PEST_LABELS_PATH)

_pest_model = None
_pest_labels = None


def get_pest_model():
    global _pest_model, _pest_labels
    if _pest_model is None:
        _pest_model = load_model(PEST_MODEL_PATH)
        with open(PEST_LABELS_PATH) as f:
            _pest_labels = json.load(f)
    return _pest_model, _pest_labels


def predict_pest(image_path):
    model, labels = get_pest_model()

    img = keras_image.load_img(image_path, target_size=(128, 128))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)[0]
    predicted_index = int(np.argmax(predictions))
    confidence = float(predictions[predicted_index]) * 100

    return {
        "predicted_pest": labels[str(predicted_index)],
        "confidence": round(confidence, 2)
    }