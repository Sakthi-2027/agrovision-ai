from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.farm import Farm
from app.models.crop_history import CropHistory
from app.models.fertilizer_history import FertilizerHistory
from app.models.disease_history import DiseaseHistory

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.route("", methods=["GET"])
@login_required
def get_analytics():
    user_farm_ids = [f.id for f in Farm.query.filter_by(user_id=current_user.id).all()]

    if not user_farm_ids:
        return jsonify({
            "total_farms": 0,
            "total_crop_records": 0,
            "total_fertilizer_records": 0,
            "total_disease_records": 0,
            "crop_distribution": [],
            "disease_severity_breakdown": [],
            "recent_activity": []
        }), 200

    total_crop = CropHistory.query.filter(CropHistory.farm_id.in_(user_farm_ids)).count()
    total_fertilizer = FertilizerHistory.query.filter(FertilizerHistory.farm_id.in_(user_farm_ids)).count()
    total_disease = DiseaseHistory.query.filter(DiseaseHistory.farm_id.in_(user_farm_ids)).count()

    # Crop distribution: count of records grouped by crop_name
    crop_counts = db.session.query(
        CropHistory.crop_name, db.func.count(CropHistory.id)
    ).filter(CropHistory.farm_id.in_(user_farm_ids)) \
     .group_by(CropHistory.crop_name).all()

    # Disease severity breakdown: count grouped by severity
    severity_counts = db.session.query(
        DiseaseHistory.severity, db.func.count(DiseaseHistory.id)
    ).filter(DiseaseHistory.farm_id.in_(user_farm_ids)) \
     .group_by(DiseaseHistory.severity).all()

    # Recent activity: latest 5 crop history entries as a simple timeline
    recent_crops = CropHistory.query.filter(CropHistory.farm_id.in_(user_farm_ids)) \
        .order_by(CropHistory.created_at.desc()).limit(5).all()

    return jsonify({
        "total_farms": len(user_farm_ids),
        "total_crop_records": total_crop,
        "total_fertilizer_records": total_fertilizer,
        "total_disease_records": total_disease,
        "crop_distribution": [{"name": name or "Unspecified", "count": count} for name, count in crop_counts],
        "disease_severity_breakdown": [{"severity": sev or "Unspecified", "count": count} for sev, count in severity_counts],
        "recent_activity": [
            {"crop_name": c.crop_name, "season": c.season, "created_at": c.created_at.isoformat()}
            for c in recent_crops
        ]
    }), 200