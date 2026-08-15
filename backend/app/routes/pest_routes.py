import os
import uuid
from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.ml_service import predict_pest

pest_bp = Blueprint("pest", __name__, url_prefix="/api/pest-prediction")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@pest_bp.route("", methods=["POST"])
@login_required
def predict_pest_route():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Please upload a valid image file (png, jpg, jpeg)"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = predict_pest(filepath)
    finally:
        os.remove(filepath)  

    return jsonify(result), 200