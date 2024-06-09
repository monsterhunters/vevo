import os
import json
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def refresh_token():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/drive'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials available.")

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds.token

def ping_colab(notebook_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(notebook_url, headers=headers)
    if response.status_code == 200:
        print("Successfully pinged the Colab notebook.")
    else:
        print(f"Failed to ping the Colab notebook. Status code: {response.status_code}")

if __name__ == "__main__":
    notebook_url = "YOUR_COLAB_NOTEBOOK_URL"

    # Save the credentials file from GitHub Secrets
    with open('credentials.json', 'w') as f:
        f.write(os.getenv('GOOGLE_OAUTH2_CREDENTIALS'))

    access_token = refresh_token()
    ping_colab(notebook_url, access_token)
