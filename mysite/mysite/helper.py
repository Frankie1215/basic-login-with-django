import httplib2
import base64
from oauth2client.file import Storage
from apiclient import discovery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def get_gmail_service():
    store = Storage(settings.GMAIL_SEND_CREDENTIAL_PATH)
    credentials = store.get()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    return service


def create_message(sender, to, subject, msgplain=None, msghtml=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    if msgplain:
        msg.attach(MIMEText(msgplain, 'plain'))

    if msghtml:
        msg.attach(MIMEText(msghtml, 'html'))

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body


def send_message_internal(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    return message
