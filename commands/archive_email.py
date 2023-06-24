from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .base_command import BaseCommand

class CommandArchiveEmail(BaseCommand):
    def __init__(self):
        self.name = "archive_email"
        self.metadata = [
            {
                "name": f"{self.name}",
                "description": "Archive an email based on its subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "The specific subject of the email to be archived"
                        }
                    },
                    "required": ["subject"]
                }
            }
        ]
        super().__init__(f"{self.name}", self.metadata)

    def execute(self, subject):
        """Archive an email based on its subject."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.get_gmail_client_id(),
            "client_secret": self.get_gmail_client_secret(),
            "refresh_token": self.get_gmail_refresh_token()
        })

        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q=f"subject:{subject}").execute()
        messages = results.get('messages', [])
        
        if not messages:
            return f"No emails found with subject: {subject}"
        
        message = service.users().messages().modify(userId='me', id=messages[0]['id'], body={'removeLabelIds': ['INBOX']}).execute()
        return f"Archived email with subject: {subject}"
