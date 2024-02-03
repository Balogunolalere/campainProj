from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from .models import Campaign
from .utils import generate_unique_id
from .config import DETA_PROJECT_KEY
from deta import Deta
from datetime import datetime

router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for subscribers and campaigns
campaigns_db = deta.Base('campaigns')


@router.post("/campaigns", description="Create a new email campaign.")
async def create_campaign(campaign: Campaign):
    """Create a new email campaign."""
    campaign.id = generate_unique_id()
    new_campaign = campaigns_db.put(campaign.dict(), key=campaign.id)
    return new_campaign

@router.get("/campaigns", description="Get all email campaigns.")
async def get_campaigns():
    """Get all email campaigns."""
    return list(campaigns_db.fetch())

# @router.post("/lists", description="Create a new list.")
# async def create_list(list: EmailList):
#     """Create a new list."""
#     list.id = generate_unique_id()
#     new_list = lists_db.put(list.dict(), key=list.id)
#     return new_list

# @router.get("/lists", description="Get all lists.")
# async def get_lists():
#     """Get all lists."""
#     return list(lists_db.fetch())

# @router.post("/send_email", description="Send an email campaign to all subscribers in the list.")
# async def send_email(campaign_id: str):
#     """Send an email campaign to all subscribers in the list."""
#     campaign = campaigns_db.get(campaign_id)
#     if not campaign:
#         raise HTTPException(status_code=404, detail="Campaign not found")
#     subscribers = list(subscribers_db.fetch())
#     for subscriber in subscribers:
#         try:
#             send_transactional_email(subscriber['email'], campaign['subject'], campaign['content'])
#         except Exception as e:
#             handle_error(e)
#     return {"message": "Emails sent successfully"}