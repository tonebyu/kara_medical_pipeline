from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def get_top_products(db: Session, limit: int = 10):
    return (
        db.query(models.ImageDetection.object_class, func.count().label("count"))
        .group_by(models.ImageDetection.object_class)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )

def get_channel_activity(db: Session, channel_name: str):
    return (
        db.query(models.Message.channel_name, func.count().label("message_count"))
        .filter(models.Message.channel_name == channel_name)
        .group_by(models.Message.channel_name)
        .first()
    )

def search_messages(db: Session, query: str):
    return (
        db.query(models.Message)
        .filter(models.Message.content.ilike(f"%{query}%"))
        .all()
    )
