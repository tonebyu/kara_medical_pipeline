from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TopProduct(BaseModel):
    object_class: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int

class MessageSearch(BaseModel):
    message_id: int
    channel_name: str
    content: str
    timestamp: datetime
