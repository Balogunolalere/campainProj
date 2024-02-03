# config.py
# import os and dotenv
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Deta
DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")
# SMTP
SMTP_SERVER = "your_smtp_server"
SMTP_PORT = 587
SMTP_USERNAME = "your_email_username"
SMTP_PASSWORD = "your_email_password"

# Transactional Email
TRANSACTIONAL_EMAIL_API_KEY = "your_transactional_email_api_key"
TRANSACTIONAL_EMAIL_SENDER_EMAIL = "your_verified_sender_email"