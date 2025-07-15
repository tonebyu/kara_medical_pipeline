from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Message(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {'schema': 'staging'}

    message_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {'schema': 'staging'}

    message_id = Column(Integer, primary_key=True, index=True)
    image_file = Column(String)
    object_class = Column(String)
    confidence_score = Column(Float)
