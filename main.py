import logging
import uvicorn
from fastapi import FastAPI
from app import config
import smtplib
from email.mime.text import MIMEText
from deta import Deta
from app.routes.subscriber import router as subscriber_router
from app.routes.campaign import router as campaign_router
from app.routes.emaillist import router as emaillist_router


app = FastAPI(title="Email Marketing App")

# Configure logging format
LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s"

# Configure logging level (e.g., DEBUG, INFO, WARNING)
LOGGING_LEVEL = logging.INFO

# Create a logger for the application
logger = logging.getLogger("email_marketing_app")

# Set logging format and level
logger.addHandler(logging.StreamHandler())
logger.setLevel(LOGGING_LEVEL)
logger.propagate = False  # Avoid duplicate logging in FastAPI

# Import and mount API routes
app.include_router(subscriber_router, prefix="/subscriber", tags=["Subscribers Route"])
app.include_router(campaign_router, prefix="/campaign", tags=["Campaign Route"])
app.include_router(emaillist_router, prefix="/emaillist", tags=["Email List Route"])

# Initialize Deta with project key
deta = Deta(config.DETA_PROJECT_KEY)

# Initialize SMTP configuration
smtp_server = config.SMTP_SERVER
smtp_port = config.SMTP_PORT
email_username = config.SMTP_USERNAME
email_password = config.SMTP_PASSWORD

# Transactional Email
transactional_email_api_key = config.TRANSACTIONAL_EMAIL_API_KEY
transactional_email_sender_email = config.TRANSACTIONAL_EMAIL_SENDER_EMAIL

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Function to send transactional emails using SMTP
def send_transactional_email(recipient_email: str, subject: str, content: str):
    """Sends a transactional email using SMTP."""
    message = MIMEText(content, "html")  # Assuming HTML content
    message["Subject"] = subject
    message["From"] = email_username
    message["To"] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, recipient_email, message.as_string())
