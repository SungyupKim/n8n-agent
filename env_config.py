# Environment configuration for n8n webhook testing
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# n8n Webhook Configuration
N8N_USERNAME = os.getenv('N8N_USERNAME')
N8N_PASSWORD = os.getenv('N8N_PASSWORD')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

def get_auth_credentials():
    """Get authentication credentials from environment variables"""
    if not N8N_USERNAME or not N8N_PASSWORD:
        raise ValueError("N8N_USERNAME and N8N_PASSWORD must be set in environment variables or .env file")
    return N8N_USERNAME, N8N_PASSWORD

def get_webhook_url():
    """Get webhook URL from environment variables"""
    if not N8N_WEBHOOK_URL:
        raise ValueError("N8N_WEBHOOK_URL must be set in environment variables or .env file")
    return N8N_WEBHOOK_URL
