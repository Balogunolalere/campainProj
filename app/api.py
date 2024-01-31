from fastapi import APIRouter, HTTPException
from typing import List
from .models import Subscriber, Campaign, EmailList
from .utils import validate_email, generate_unique_id, send_transactional_email, handle_error
from .config import DETA_PROJECT_KEY
from deta import Deta

router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for subscribers and campaigns
subscribers_db = deta.Base('subscribers')
campaigns_db = deta.Base('campaigns')
lists_db = deta.Base('lists')

@router.post("/subscribers", response_model=Subscriber, description="Create a new subscriber.")
async def create_subscriber(subscriber: Subscriber):
    """Create a new subscriber."""
    if not validate_email(subscriber.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    subscriber.id = generate_unique_id()
    new_subscriber = subscribers_db.put(subscriber.dict(), key=subscriber.id)
    return new_subscriber

@router.get("/subscribers", response_model=list[Subscriber], description="Get all subscribers.")
async def get_subscribers():
    """Get all subscribers."""
    return list(subscribers_db.fetch())

@router.post("/campaigns", response_model=Campaign, description="Create a new email campaign.")
async def create_campaign(campaign: Campaign):
    """Create a new email campaign."""
    campaign.id = generate_unique_id()
    new_campaign = campaigns_db.put(campaign.dict(), key=campaign.id)
    return new_campaign

@router.get("/campaigns", response_model=list[Campaign], description="Get all email campaigns.")
async def get_campaigns():
    """Get all email campaigns."""
    return list(campaigns_db.fetch())

@router.post("/lists", response_model=EmailList, description="Create a new list.")
async def create_list(list: EmailList):
    """Create a new list."""
    list.id = generate_unique_id()
    new_list = lists_db.put(list.dict(), key=list.id)
    return new_list

@router.get("/lists", response_model=list[EmailList], description="Get all lists.")
async def get_lists():
    """Get all lists."""
    return list(lists_db.fetch())

@router.post("/send_email", description="Send an email campaign to all subscribers in the list.")
async def send_email(campaign_id: str):
    """Send an email campaign to all subscribers in the list."""
    campaign = campaigns_db.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    subscribers = list(subscribers_db.fetch())
    for subscriber in subscribers:
        try:
            send_transactional_email(subscriber['email'], campaign['subject'], campaign['content'])
        except Exception as e:
            handle_error(e)
    return {"message": "Emails sent successfully"}