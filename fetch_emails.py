from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import os
from email import message_from_bytes
from gmail_auth import authenticate_gmail

def fetch_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']

        # Extract body (plain text or HTML)
        body = ""
        payload = msg_data['payload']
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/html':
                    body = part['body'].get('data', '')
                    break
                elif part.get('mimeType') == 'text/plain' and not body:
                    body = part['body'].get('data', '')
        else:
            body = payload.get('body', {}).get('data', '')
        if body:
            try:
                body = base64.urlsafe_b64decode(body).decode('utf-8', errors='ignore')
            except Exception:
                body = "(Could not decode body)"

        email_info = {
            'From': next((h['value'] for h in headers if h['name'] == 'From'), 'N/A'),
            'Subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'N/A'),
            'Date': next((h['value'] for h in headers if h['name'] == 'Date'), 'N/A'),
            'Snippet': msg_data.get('snippet', ''),
            'Body': body
        }

        email_list.append(email_info)
    return email_list

# 🔍 Test the script
if __name__ == '__main__':
    emails = fetch_emails()
    for email in emails:
        print("📧 From:", email['From'])
        print("📝 Subject:", email['Subject'])
        print("📅 Date:", email['Date'])
        print("🔍 Snippet:", email['Snippet'])
        print("------")
