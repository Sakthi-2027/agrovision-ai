from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.notification import Notification

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


@notification_bp.route("", methods=["GET"])
@login_required
def list_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id) \
        .order_by(Notification.created_at.desc()).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return jsonify({
        "unread_count": unread_count,
        "notifications": [n.to_dict() for n in notifications]
    }), 200


@notification_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@login_required
def mark_as_read(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.is_read = True
    db.session.commit()
    return jsonify(notification.to_dict()), 200


@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200