# Environment configuration for n8n webhook testing
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# n8n Webhook Configuration
# Support both old and new environment variable names for backward compatibility
WEBHOOK_USERNAME = os.getenv('WEBHOOK_USERNAME') or os.getenv('N8N_USERNAME')
WEBHOOK_PASSWORD = os.getenv('WEBHOOK_PASSWORD') or os.getenv('N8N_PASSWORD')
WEBHOOK_URL = os.getenv('WEBHOOK_URL') or os.getenv('N8N_WEBHOOK_URL')

def get_auth_credentials():
    """Get authentication credentials from environment variables"""
    if not WEBHOOK_USERNAME or not WEBHOOK_PASSWORD:
        raise ValueError("WEBHOOK_USERNAME and WEBHOOK_PASSWORD (or N8N_USERNAME and N8N_PASSWORD) must be set in environment variables or .env file")
    return WEBHOOK_USERNAME, WEBHOOK_PASSWORD

def get_webhook_url():
    """Get webhook URL from environment variables"""
    if not WEBHOOK_URL:
        raise ValueError("WEBHOOK_URL (or N8N_WEBHOOK_URL) must be set in environment variables or .env file")
    return WEBHOOK_URL
