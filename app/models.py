from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Status(str, Enum):
    draft = "draft"
    scheduled = "scheduled"
    sent = "sent"

class Subscriber(BaseModel):
    email: EmailStr = Field(...)
    subscribed: bool = Field(...)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    source: Optional[str] = Field(None)

class SubscriberUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None)
    subscribed: Optional[bool] = Field(None)
    updated_at: Optional[datetime] = Field(None)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    source: Optional[str] = Field(None)

class Campaign(BaseModel):
    subject: str = Field(...)
    content: str = Field(...)
    list_ids: List[str] = Field(...)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)
    status: Status = Field(Status.draft)
    scheduled_at: Optional[datetime] = Field(None)
    sent_at: Optional[datetime] = Field(None)
    sender_id: Optional[str] = Field(None)

class CampaignUpdate(BaseModel):
    subject: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    list_ids: Optional[List[str]] = Field(None)
    updated_at: Optional[datetime] = Field(None)
    status: Optional[Status] = Field(None)
    scheduled_at: Optional[datetime] = Field(None)
    sent_at: Optional[datetime] = Field(None)
    sender_id: Optional[str] = Field(None)

class EmailList(BaseModel):
    name: str = Field(...)
    description: Optional[str] = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)

class EmailListUpdate(BaseModel):
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    updated_at: Optional[datetime] = Field(None)


