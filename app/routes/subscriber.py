from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from ..models import Subscriber, SubscriberUpdate
from ..utils import generate_unique_id, handle_error
from ..config import DETA_PROJECT_KEY
from deta import Deta
from datetime import datetime

router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for subscribers
subscribers_db = deta.Base('subscribers')

def get_subscriber_by_key(email: str):
    subscriber = subscribers_db.fetch({"email": email}).items
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber[0]

@router.post("/", description="Create a new subscriber.", response_model=Subscriber)
async def create_subscriber(subscriber: Subscriber):
    """Create a new subscriber."""
    existing_subscriber = subscribers_db.fetch({"email": subscriber.email}).items
    if existing_subscriber:
        raise HTTPException(status_code=400, detail="Email already in use")

    key_ = generate_unique_id()
    subscriber.created_at = datetime.now().isoformat()
    subscriber.subscribed = True
    new_subscriber = subscribers_db.put(subscriber.dict(), key=key_)
    return new_subscriber

@router.post("/upload_emails", description="Reads emails from a TXT file and uploads them to Deta", status_code=status.HTTP_201_CREATED)
async def upload_emails(file: UploadFile = File(...)):
    """Reads emails from a TXT file and uploads them to Deta in batches of 25."""

    emails = []
    contents = await file.read()
    for email in contents.decode().splitlines():
        email = email.strip()
        try:
            subscriber = Subscriber(email=email, subscribed=True)
            key_ = generate_unique_id()
            subscriber.created_at = datetime.now().isoformat()
            subscriber_dict = subscriber.dict()
            subscriber_dict["key"] = key_  # Add the key to the subscriber dictionary
            emails.append(subscriber_dict)
        except ValueError:
            print(f"Invalid email: {email}")

    if emails:
        index = 0
        while index < len(emails):
            batch = emails[index:index + 25]
            try:
                subscribers_db.put_many(batch)
            except Exception as e:
                handle_error(e)
            index += 25

        return {"message": "Emails uploaded successfully"}
    else:
        return {"message": "No valid emails found in the file"}

@router.get("/", description="Get all subscribers.", response_model=List[Subscriber])
async def get_subscribers():
    """Get all subscribers."""
    subscribers = subscribers_db.fetch().items
    return subscribers

@router.get("/{email}", description="Get a subscriber by email.", response_model=Subscriber)
async def get_subscriber(email: str):
    """Get a subscriber by email."""
    return get_subscriber_by_key(email)

@router.patch("/{email}", description="Update a subscriber.", response_model=Subscriber)
async def update_subscriber(email: str, subscriber_data: SubscriberUpdate):
    """Update a subscriber."""
    subscriber = get_subscriber_by_key(email)
    update_data = subscriber_data.dict(exclude_unset=True)

    # Only update fields that were passed in the request
    for field, value in update_data.items():
        subscriber[field] = value

    # Convert datetime objects to strings
    if 'created_at' in subscriber and isinstance(subscriber['created_at'], datetime):
        subscriber['created_at'] = subscriber['created_at'].isoformat()
    if 'updated_at' in subscriber and isinstance(subscriber['updated_at'], datetime):
        subscriber['updated_at'] = subscriber['updated_at'].isoformat()

    subscribers_db.put(subscriber, key=subscriber["key"])
    return subscriber

@router.delete("/{email}", description="Delete a subscriber by email.")
async def delete_subscriber(email: str):
    """Delete a subscriber by email."""
    subscriber = get_subscriber_by_key(email)
    subscribers_db.delete(subscriber["key"])
    return {"message": "Subscriber deleted successfully"}