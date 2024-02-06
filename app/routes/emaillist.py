from fastapi import APIRouter, HTTPException
from ..models import EmailList, EmailListUpdate
from ..config import DETA_PROJECT_KEY
from deta import Deta
from datetime import datetime
from typing import List


router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for email lists
email_lists_db = deta.Base('email_lists')

def get_email_list_by_name(name: str):
    email_list = email_lists_db.fetch({"name": name}).items
    if not email_list:
        raise HTTPException(status_code=404, detail="Email list not found")
    return email_list[0]

@router.post("/", description="Create a new email list.", response_model=EmailList)
async def create_email_list(email_list: EmailList):
    """Create a new email list."""
    email_list.created_at = datetime.now().isoformat()
    email_lists_db.put(email_list.dict(), key=email_list.name)
    return email_list

@router.get("/", description="Get all email lists.", response_model=List[EmailList])
async def get_email_lists():
    """Get all email lists."""
    email_lists = email_lists_db.fetch().items
    return email_lists

@router.get("/{name}", description="Get an email list by name.", response_model=EmailList)
async def get_email_list(name: str):
    """Get an email list by name."""
    return get_email_list_by_name(name)

@router.patch("/{name}", description="Update an email list.", response_model=EmailList)
async def update_email_list(name: str, email_list_data: EmailListUpdate):
    """Update an email list."""
    email_list = get_email_list_by_name(name)
    update_data = email_list_data.dict(exclude_unset=True)

    # Only update fields that were passed in the request
    for field, value in update_data.items():
        email_list[field] = value

    # Convert datetime objects to strings
    if 'updated_at' in email_list and isinstance(email_list['updated_at'], datetime):
        email_list['updated_at'] = email_list['updated_at'].isoformat()

    email_lists_db.put(email_list, key=email_list["name"])
    return email_list

@router.delete("/{name}", description="Delete an email list by name.")
async def delete_email_list(name: str):
    """Delete an email list by name."""
    email_list = get_email_list_by_name(name)
    email_lists_db.delete(email_list["name"])
    return {"message": "Email list deleted successfully"}