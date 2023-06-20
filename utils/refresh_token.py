import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    with open('api_keys.json') as f:
        keys = json.load(f)
        gmail_keys = keys['gmail']

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"web": gmail_keys},
                SCOPES, 
                redirect_uri=gmail_keys['redirect_uris'][0]
            )
            creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        # Store the refresh token
        gmail_keys['refresh_token'] = creds.refresh_token
        with open('api_keys.json', 'w') as f:
            json.dump(keys, f, indent=4)

    print("Refresh token:", creds.refresh_token)

if __name__ == '__main__':
    main()
