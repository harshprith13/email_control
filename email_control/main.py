from gmail_service import authenticate_gmail
from email_utils import list_emails, send_email
import schedule
import time


# email_utils.py

def list_spam_emails(service, max_results=10):
    # List emails from the Spam folder
    results = service.users().messages().list(
        userId='me', labelIds=['SPAM'], maxResults=max_results
    ).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} spam messages.")
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print(f"Spam Message Subject: {msg['snippet']}")
        # Automatically move spam to inbox
        move_to_inbox(service, message['id'])

def move_to_inbox(service, message_id):
    # Move a message from Spam to Inbox
    service.users().messages().modify(
        userId='me', id=message_id, body={'addLabelIds': ['INBOX'], 'removeLabelIds': ['SPAM']}
    ).execute()
    print(f"Message {message_id} moved to Inbox.")

def check_emails():
    gmail_service = authenticate_gmail()
    print("Checking Inbox...")
    list_emails(gmail_service, label_ids=['INBOX'], max_results=5)

def send_test_email():
    gmail_service = authenticate_gmail()
    print("Sending Test Email...")
    send_email(gmail_service, "recipient@example.com", "Test Subject", "This is a test email!")

# Schedule tasks
schedule.every(1).minutes.do(check_emails)
schedule.every().day.at("10:25").do(send_test_email)

if __name__ == "__main__":
    print("Email Control Program Running...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    gmail_service = authenticate_gmail()
    print("Checking Spam...")
    list_spam_emails(gmail_service, max_results=5)  # List up to 5 spam emails and move them to Inbox