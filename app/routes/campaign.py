from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Campaign, CampaignUpdate
from ..utils import generate_unique_id
from ..config import DETA_PROJECT_KEY
from deta import Deta
from datetime import datetime

router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for campaigns
campaigns_db = deta.Base('campaigns')

def get_campaign_by_key(key: str):
    campaign = campaigns_db.get(key)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/", description="Create a new campaign.", response_model=Campaign)
async def create_campaign(campaign: Campaign):
    """Create a new campaign."""
    existing_campaign = campaigns_db.fetch({"subject": campaign.subject}).items
    if existing_campaign:
        raise HTTPException(status_code=400, detail="Campaign with this subject already exists")

    key_ = generate_unique_id()
    campaign.created_at = datetime.now().isoformat()
    new_campaign = campaigns_db.put(campaign.dict(), key=key_)
    return new_campaign

@router.get("/", description="Get all campaigns.", response_model=List[Campaign])
async def get_campaigns():
    """Get all campaigns."""
    campaigns = campaigns_db.fetch().items
    return campaigns

@router.get("/{key}", description="Get a campaign by key.", response_model=Campaign)
async def get_campaign(key: str):
    """Get a campaign by key."""
    return get_campaign_by_key(key)

@router.patch("/{key}", description="Update a campaign.", response_model=Campaign)
async def update_campaign(key: str, campaign_data: CampaignUpdate):
    """Update a campaign."""
    campaign = get_campaign_by_key(key)
    update_data = campaign_data.dict(exclude_unset=True)

    # Only update fields that were passed in the request
    for field, value in update_data.items():
        campaign[field] = value

    # Convert datetime objects to strings
    if 'created_at' in campaign and isinstance(campaign['created_at'], datetime):
        campaign['created_at'] = campaign['created_at'].isoformat()

    # Update the 'updated_at' field with the current time
    campaign['updated_at'] = datetime.now().isoformat()

    campaigns_db.put(campaign, key=campaign["key"])
    return campaign

@router.delete("/{key}", description="Delete a campaign by key.")
async def delete_campaign(key: str):
    """Delete a campaign by key."""
    campaign = get_campaign_by_key(key)
    campaigns_db.delete(key)
    return {"detail": "Campaign deleted"}

