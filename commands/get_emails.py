from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_emails(self, num_emails):
        """Get the subjects of the num_emails most recent emails in the primary inbox."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.gmail_client_id,
            "client_secret": self.gmail_client_secret,
            "refresh_token": self.gmail_refresh_token
        })

        service = build('gmail', 'v1', credentials=creds)

        # Call the Gmail API to get messages from primary inbox
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

        # join the subjects into a single string
        return '\n'.join(email_subjects)