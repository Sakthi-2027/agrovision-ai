from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.farm import Farm
from app.models.crop_history import CropHistory
from app.models.fertilizer_history import FertilizerHistory
from app.models.disease_history import DiseaseHistory
from app.services.notification_service import create_notification

farm_bp = Blueprint("farms", __name__, url_prefix="/api/farms")


def get_owned_farm_or_none(farm_id):
    """Shared helper: returns the farm only if it belongs to the current user."""
    return Farm.query.filter_by(id=farm_id, user_id=current_user.id).first()


def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None


# ---------------- FARMS ----------------

@farm_bp.route("", methods=["GET"])
@login_required
def list_farms():
    farms = Farm.query.filter_by(user_id=current_user.id).order_by(Farm.created_at.desc()).all()
    return jsonify([f.to_dict() for f in farms]), 200


@farm_bp.route("", methods=["POST"])
@login_required
def create_farm():
    data = request.get_json()
    farm_name = data.get("farm_name")

    if not farm_name:
        return jsonify({"error": "farm_name is required"}), 400

    farm = Farm(
        user_id=current_user.id,
        farm_name=farm_name,
        location=data.get("location"),
        size_in_acres=data.get("size_in_acres"),
        soil_type=data.get("soil_type")
    )
    db.session.add(farm)
    db.session.commit()

    return jsonify(farm.to_dict()), 201


@farm_bp.route("/<int:farm_id>", methods=["PUT"])
@login_required
def update_farm(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    data = request.get_json()
    farm.farm_name = data.get("farm_name", farm.farm_name)
    farm.location = data.get("location", farm.location)
    farm.size_in_acres = data.get("size_in_acres", farm.size_in_acres)
    farm.soil_type = data.get("soil_type", farm.soil_type)

    db.session.commit()
    return jsonify(farm.to_dict()), 200


@farm_bp.route("/<int:farm_id>", methods=["DELETE"])
@login_required
def delete_farm(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    db.session.delete(farm)
    db.session.commit()
    return jsonify({"message": "Farm deleted"}), 200


# ---------------- CROP HISTORY ----------------

@farm_bp.route("/<int:farm_id>/crop-history", methods=["GET"])
@login_required
def list_crop_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    records = CropHistory.query.filter_by(farm_id=farm_id).order_by(CropHistory.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records]), 200


@farm_bp.route("/<int:farm_id>/crop-history", methods=["POST"])
@login_required
def create_crop_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    data = request.get_json()
    if not data.get("crop_name"):
        return jsonify({"error": "crop_name is required"}), 400

    record = CropHistory(
        farm_id=farm_id,
        crop_name=data.get("crop_name"),
        season=data.get("season"),
        planting_date=parse_date(data.get("planting_date")),
        harvest_date=parse_date(data.get("harvest_date")),
        notes=data.get("notes")
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@farm_bp.route("/<int:farm_id>/crop-history/<int:record_id>", methods=["DELETE"])
@login_required
def delete_crop_history(farm_id, record_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    record = CropHistory.query.filter_by(id=record_id, farm_id=farm_id).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Crop history record deleted"}), 200


# ---------------- FERTILIZER HISTORY ----------------

@farm_bp.route("/<int:farm_id>/fertilizer-history", methods=["GET"])
@login_required
def list_fertilizer_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    records = FertilizerHistory.query.filter_by(farm_id=farm_id).order_by(FertilizerHistory.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records]), 200


@farm_bp.route("/<int:farm_id>/fertilizer-history", methods=["POST"])
@login_required
def create_fertilizer_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    data = request.get_json()
    if not data.get("fertilizer_name"):
        return jsonify({"error": "fertilizer_name is required"}), 400

    record = FertilizerHistory(
        farm_id=farm_id,
        fertilizer_name=data.get("fertilizer_name"),
        quantity=data.get("quantity"),
        unit=data.get("unit"),
        application_date=parse_date(data.get("application_date")),
        notes=data.get("notes")
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@farm_bp.route("/<int:farm_id>/fertilizer-history/<int:record_id>", methods=["DELETE"])
@login_required
def delete_fertilizer_history(farm_id, record_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    record = FertilizerHistory.query.filter_by(id=record_id, farm_id=farm_id).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Fertilizer history record deleted"}), 200


# ---------------- DISEASE HISTORY ----------------

@farm_bp.route("/<int:farm_id>/disease-history", methods=["GET"])
@login_required
def list_disease_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    records = DiseaseHistory.query.filter_by(farm_id=farm_id).order_by(DiseaseHistory.created_at.desc()).all()
    return jsonify([r.to_dict() for r in records]), 200


@farm_bp.route("/<int:farm_id>/disease-history", methods=["POST"])
@login_required
def create_disease_history(farm_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    data = request.get_json()
    if not data.get("disease_name"):
        return jsonify({"error": "disease_name is required"}), 400

    record = DiseaseHistory(
        farm_id=farm_id,
        disease_name=data.get("disease_name"),
        crop_affected=data.get("crop_affected"),
        severity=data.get("severity"),
        detected_date=parse_date(data.get("detected_date")),
        notes=data.get("notes")
    )
    db.session.add(record)
    db.session.commit()

    # Trigger a notification for high-severity disease reports
    if data.get("severity") == "High":
        create_notification(
            user_id=current_user.id,
            title=f"High severity disease detected: {record.disease_name}",
            message=f"{record.disease_name} was reported on {farm.farm_name}"
                    + (f" affecting {record.crop_affected}" if record.crop_affected else "") + ".",
            category="disease"
        )

    return jsonify(record.to_dict()), 201


@farm_bp.route("/<int:farm_id>/disease-history/<int:record_id>", methods=["DELETE"])
@login_required
def delete_disease_history(farm_id, record_id):
    farm = get_owned_farm_or_none(farm_id)
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    record = DiseaseHistory.query.filter_by(id=record_id, farm_id=farm_id).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Disease history record deleted"}), 200