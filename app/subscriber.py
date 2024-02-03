from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from .models import Subscriber, UpdateSubscriber
from .utils import generate_unique_id, handle_error
from .config import DETA_PROJECT_KEY
from deta import Deta
from datetime import datetime

router = APIRouter()

# Initialize Deta with project key
deta = Deta(DETA_PROJECT_KEY)

# Deta Base for subscribers and campaigns
subscribers_db = deta.Base('subscribers')


@router.post("/subscribers", description="Create a new subscriber.", response_model=Subscriber)
async def create_subscriber(subscriber: Subscriber):
    """Create a new subscriber."""
    key_ = generate_unique_id()
    subscriber.created_at = datetime.now()  # Assign datetime object
    subscriber.subscribed = True

    # Convert created_at to ISO 8601 string before serialization
    subscriber_dict = subscriber.dict(exclude_unset=True)  # Exclude unset fields
    subscriber_dict["created_at"] = subscriber.created_at.date().isoformat() # Convert to string

    new_subscriber = subscribers_db.put(subscriber_dict, key=key_)
    return new_subscriber


@router.post("/upload_emails", description="Reads emails from a TXT file and uploads them to Deta", status_code=status.HTTP_201_CREATED)
async def upload_emails(file: UploadFile = File(...)):
    """Reads emails from a TXT file and uploads them to Deta in batches of 25."""

    emails = []
    contents = await file.read()
    for email in contents.decode().splitlines():
        email = email.strip()
        try:
            subscriber = Subscriber(email=email, subscribed=True)  # Create Subscriber instance
            key_ = generate_unique_id()  # Assign unique ID
            subscriber.created_at = datetime.now()  # Assign datetime object

            # Convert created_at to ISO 8601 string and exclude unset fields
            subscriber_dict = subscriber.dict(exclude_unset=True)
            subscriber_dict["created_at"] = subscriber.created_at.date().isoformat()  # Convert to string

            # Include the key in the dictionary
            subscriber_dict["key"] = key_

            emails.append(subscriber_dict)  # Append serialized dictionary
        except ValueError:
            print(f"Invalid email: {email}")

    if emails:
        index = 0
        while index < len(emails):
            batch = emails[index:index + 25]
            try:
                subscribers_db.put_many(batch)  # Store with included keys
            except Exception as e:
                handle_error(e)
            index += 25

        return {"message": "Emails uploaded successfully"}
    else:
        return {"message": "No valid emails found in the file"}


@router.get("/subscribers", description="Get all subscribers.", response_model=List[Subscriber])
async def get_subscribers():
    """Get all subscribers."""
    subscribers = subscribers_db.fetch().items  # Access the items property to get the iterable data
    return subscribers

@router.get("{email}", description="Get a subscriber by email.", response_model=Subscriber)
async def get_subscriber(email: str):
    """Get a subscriber by email."""
    # Query the database for the subscriber with the given email eg first_result = db.fetch({"age?lt": 30})
    subscriber = subscribers_db.fetch({"email": email}).items
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber[0]
    
@router.patch("/subscribers/{email}", description="Update the subscription status of a subscriber.", response_model=Subscriber)
async def update_subscription(email: str, subscriber_data: UpdateSubscriber):
    """Update the subscription status of a subscriber."""

    # Query the database for the subscriber with the given email
    subscriber = subscribers_db.fetch({"email": email}).items
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    # Extract the key of the subscriber from the list of dictionaries
    key = subscriber[0]["key"]

    # Update only the `subscribed` field
    subscriber_db = subscribers_db.get(key)
    subscriber_db["subscribed"] = subscriber_data.subscribed
    updated_subscriber = subscribers_db.put(subscriber_db, key)

    return updated_subscriber

@router.delete("{email}", description="Delete a subscriber by email.")
async def delete_subscriber(email: str):
    """Delete a subscriber by email."""

    # Query the database for the subscriber with the given email
    subscriber = subscribers_db.fetch({"email": email}).items
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    # Extract the key of the subscriber from the list of dictionaries
    key = subscriber[0]["key"]  # Access the key from the first (and only) dictionary

    # Delete the subscriber from the database using the extracted key
    subscribers_db.delete(key)

    return {"message": "Subscriber deleted successfully"}
    

