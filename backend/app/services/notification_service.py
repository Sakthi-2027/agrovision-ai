from app.extensions import db
from app.models.notification import Notification


def create_notification(user_id, title, message, category="system"):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        category=category
    )
    db.session.add(notification)
    db.session.commit()
    return notification