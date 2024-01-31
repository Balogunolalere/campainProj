import uuid
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app import config  # import the config module

# Function to validate email addresses
def validate_email(email: str) -> bool:
    """Validates an email address."""
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email) is not None

# Function to generate unique IDs
def generate_unique_id() -> str:
    """Generates a unique ID."""
    return str(uuid.uuid4())

# Function to send transactional emails (implementation depends on chosen service)
def send_transactional_email(recipient_email: str, subject: str, content: str, **kwargs):
    """Sends a transactional email."""
    # Set up SMTP server
    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)

    # Create message
    msg = MIMEMultipart()
    msg['From'] = config.SMTP_USERNAME
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))

    # Send email
    server.send_message(msg)
    server.quit()

# Function to handle errors gracefully
def handle_error(error: Exception) -> dict:
    """Handles errors and returns a JSON response."""
    return {"error": str(error)}