from pydantic import BaseModel,validator
import re
from datetime import datetime
from typing import Optional

class Subscriber(BaseModel):
    email: str
    subscribed: bool
    created_at: datetime 

class UpdateSubscriber(Subscriber):
    subscribed: Optional[bool] = None


class Campaign(BaseModel):
    subject: str
    content: str
    list_ids: list[str]

    @validator("list_ids")
    def validate_list_ids(cls, value):
        # List ID validation logic (e.g., regex)
        raise ValueError("Invalid list ID") if not value or not re.match("^[a-zA-Z0-9]+$", value) else value
    
    class Config:
        # Customize error messages for validation failures
        error_messages = {
            "list_ids": {"invalid": "Please enter a valid list ID."},
        }


class EmailList(BaseModel):
    name: str
    description: str = None
    created_at: datetime = None
    updated_at: datetime = None

    @validator("name")
    def validate_name(cls, value):
        # List name validation logic (e.g., regex)
        raise ValueError("Invalid list name") if not value or not re.match("^[a-zA-Z0-9]+$", value) else value

    class Config:
        # Customize error messages for validation failures
        error_messages = {
            "name": {"invalid": "Please enter a valid list name."},
        }


    
