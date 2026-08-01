from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.farm import Farm

farm_bp = Blueprint("farms", __name__, url_prefix="/api/farms")


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
    farm = Farm.query.filter_by(id=farm_id, user_id=current_user.id).first()
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
    farm = Farm.query.filter_by(id=farm_id, user_id=current_user.id).first()
    if not farm:
        return jsonify({"error": "Farm not found"}), 404

    db.session.delete(farm)
    db.session.commit()
    return jsonify({"message": "Farm deleted"}), 200