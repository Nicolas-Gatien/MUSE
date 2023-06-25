from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from base_command import BaseCommand

class CommandGetEmails(BaseCommand):
    def __init__(self):
        self.name = "get_emails"
        self.metadata = {
                "name": f"{self.name}",
                "description": "Get all emails from the inbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num_emails": {
                            "type": "integer",
                            "description": "The number of emails to fetch (default to 10)"
                        },
                    },
                    "required": ["num_emails"],
                },
            }
        super().__init__(f"{self.name}", self.metadata)

    def execute(self, num_emails):
        """Get the subjects of the num_emails most recent emails in the primary inbox."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.get_gmail_client_id(),
            "client_secret": self.get_gmail_client_secret(),
            "refresh_token": self.get_gmail_refresh_token()
        })

        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q="in:inbox AND category:primary", maxResults=num_emails).execute()
        messages = results.get('messages', [])
        
        email_subjects = []
        if not messages:
            email_subjects.append('No new messages.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                payload = msg['payload']
                headers = payload['headers']

                for header in headers:
                    if header['name'] == 'Subject':
                        email_subjects.append(header['value'])

        return '\n'.join(email_subjects)