from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from base_command import BaseCommand

class CommandOpenEmail(BaseCommand):
    def __init__(self):
        self.name = "open_email"
        self.metadata = {
                "name": f"{self.name}",
                "description": "Open an email based on its subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "The specific subject of the email to be opened (use the full subject)"
                        }
                    },
                    "required": ["subject"]
                }
            }
        
        super().__init__(f"{self.name}", self.metadata)
    
    def execute(self, subject):
        """Open an email based on its subject."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.get_gmail_client_id(),
            "client_secret": self.get_gmail_client_secret(),
            "refresh_token": self.get_gmail_refresh_token()
        })

        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', q=f"subject:{subject}").execute()
        messages = results.get('messages', [])
        
        if messages:
            # Open the first email that matches the subject
            message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
            return f"Opened email: {message['snippet']}"
        else:
            return f"No emails found with subject: {subject}"