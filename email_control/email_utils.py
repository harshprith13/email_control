
import base64
from email.mime.text import MIMEText
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_email_sendgrid(api_key, to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key)
    from_email = Email("your_email@example.com")
    to_email = To(to_email)
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)

    response = sg.send(mail)
    print(f"Email sent to {to_email}. Response Code: {response.status_code}")
def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}
    service.users().messages().send(userId='me', body=message_body).execute()
    print(f"Email sent to {to}")
def move_to_inbox(service, message_id):
    service.users().messages().modify(
        userId='me', id=message_id, body={'addLabelIds': ['INBOX'], 'removeLabelIds': ['SPAM']}
    ).execute()
    print(f"Message {message_id} moved to Inbox.")

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
def send_bulk_emails(service, recipients, subject, body):
    for recipient in recipients:
        send_email(service, recipient, subject, body)
        print(f"Sent email to {recipient}")

def auto_reply_to_email(service, message_id, reply_subject, reply_body):
    # Get the original email to craft the reply
    original_msg = service.users().messages().get(userId='me', id=message_id).execute()
    original_from = original_msg['payload']['headers'][0]['value']  # Sender's email address

    # Craft reply message
    reply_message = MIMEText(reply_body)
    reply_message['to'] = original_from
    reply_message['subject'] = reply_subject
    raw_reply = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

    # Send reply
    service.users().messages().send(userId='me', body={'raw': raw_reply}).execute()
    print(f"Replied to {original_from}")

def list_emails(service, label_ids=['INBOX'], max_results=10):
    results = service.users().messages().list(
        userId='me', labelIds=label_ids, maxResults=max_results
    ).execute()
    messages = results.get('messages', [])
    print(f"Found {len(messages)} messages.")
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        print(f"Message Snippet: {msg['snippet']}")