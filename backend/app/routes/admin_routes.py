import os
from flask import Blueprint, jsonify
from app.utils.decorators import admin_required
from app.models.user import User
from app.models.farm import Farm
from app.models.crop_history import CropHistory
from app.models.fertilizer_history import FertilizerHistory
from app.models.disease_history import DiseaseHistory
from flask_login import current_user
from app.extensions import db

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
            "farm_count": farm_count,
            "is_active": farmer.is_active
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


@admin_bp.route("/farmers/<int:farmer_id>/deactivate", methods=["PATCH"])
@admin_required
def deactivate_farmer(farmer_id):
    if farmer_id == current_user.id:
        return jsonify({"error": "You cannot deactivate your own account"}), 400

    farmer = User.query.filter_by(id=farmer_id, role="farmer").first()
    if not farmer:
        return jsonify({"error": "Farmer not found"}), 404

    farmer.is_active = not farmer.is_active  # toggle: deactivate <-> reactivate
    db.session.commit()

    status = "deactivated" if not farmer.is_active else "reactivated"
    return jsonify({"message": f"{farmer.full_name} has been {status}", "is_active": farmer.is_active}), 200


@admin_bp.route("/farmers/<int:farmer_id>/promote", methods=["PATCH"])
@admin_required
def promote_farmer(farmer_id):
    farmer = User.query.filter_by(id=farmer_id, role="farmer").first()
    if not farmer:
        return jsonify({"error": "Farmer not found"}), 404

    farmer.role = "admin"
    db.session.commit()

    return jsonify({"message": f"{farmer.full_name} has been promoted to admin"}), 200