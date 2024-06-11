import os
import json
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def refresh_token():
    creds = None
    if os.path.exists('token.json'):
        logger.debug("Loading credentials from token.json")
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.debug("Refreshing access token")
                creds.refresh(Request())
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise Exception("Failed to refresh token")
        else:
            logger.error("No valid credentials available.")
            raise Exception("No valid credentials available.")

    with open('token.json', 'w') as token:
        logger.debug("Saving refreshed credentials to token.json")
        token.write(creds.to_json())

    return creds.token

def ping_colab(notebook_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(notebook_url, headers=headers)
    if response.status_code == 200:
        logger.info("Successfully pinged the Colab notebook.")
    else:
        logger.error(f"Failed to ping the Colab notebook. Status code: {response.status_code}")

if __name__ == "__main__":
    notebook_url = "https://colab.research.google.com/github/monsterhunters/Lora-Training-GUI/blob/main/Lora_Training_GUI_V2_2414.ipynb"

    # Save the credentials file from GitHub Secrets
    with open('credentials.json', 'w') as f:
        f.write(os.getenv('GOOGLE_OAUTH2_CREDENTIALS'))

    access_token = refresh_token()
    ping_colab(notebook_url, access_token)
