import os
from flask import Blueprint, jsonify
from app.utils.decorators import admin_required
from app.models.user import User
from app.models.farm import Farm
from app.models.crop_history import CropHistory
from app.models.fertilizer_history import FertilizerHistory
from app.models.disease_history import DiseaseHistory

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/farmers", methods=["GET"])
@admin_required
def list_farmers():
    farmers = User.query.filter_by(role="farmer").order_by(User.created_at.desc()).all()

    result = []
    for farmer in farmers:
        farm_count = Farm.query.filter_by(user_id=farmer.id).count()
        result.append({
            "id": farmer.id,
            "full_name": farmer.full_name,
            "email": farmer.email,
            "joined": farmer.created_at.isoformat(),
            "farm_count": farm_count
        })

    return jsonify(result), 200


@admin_bp.route("/stats", methods=["GET"])
@admin_required
def system_stats():
    return jsonify({
        "total_farmers": User.query.filter_by(role="farmer").count(),
        "total_farms": Farm.query.count(),
        "total_crop_records": CropHistory.query.count(),
        "total_fertilizer_records": FertilizerHistory.query.count(),
        "total_disease_records": DiseaseHistory.query.count()
    }), 200


@admin_bp.route("/datasets", methods=["GET"])
@admin_required
def list_datasets():
    
    datasets_path = os.path.join(os.getcwd(), "..", "ml", "datasets", "raw")
    datasets_path = os.path.abspath(datasets_path)

    if not os.path.exists(datasets_path):
        return jsonify({"datasets": []}), 200

    files = [
        f for f in os.listdir(datasets_path)
        if os.path.isfile(os.path.join(datasets_path, f)) and not f.startswith(".")
    ]

    return jsonify({"datasets": files}), 200