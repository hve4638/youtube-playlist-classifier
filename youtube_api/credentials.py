import json
import os
from .google_api import *

CREDENTIALS_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def make_creds(client_secret:str, token_file:str):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, CREDENTIALS_SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = make_new_creds(client_secret)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def make_new_creds(client_secret):
    flow = InstalledAppFlow.from_client_secrets_file(client_secret, CREDENTIALS_SCOPES)
    creds = flow.run_local_server(port=0)
    return creds
