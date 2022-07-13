from email.mime.application import MIMEApplication

import os.path
import base64
from urllib.error import HTTPError

import google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
import mimetypes

# Updated: 2022-02-19 19:10:39

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def send_message(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print("Message Id: {}".format(message['id']))
    return message
  except HTTPError as error:
    print("An error occurred here: %s".format(error))


def create_message_with_attachment(receiver_name, receiver_email, subject, message_text, file):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = '{} <{}>'.format(receiver_name, receiver_email)
  message['from'] = 'Bored Apes Portfolio <boredapes.portfolio@gmail.com>'
  message['subject'] = subject
  message['reply-to'] = 'Bored Apes Portfolio <boredapes.portfolio@gmail.com>'

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)

  if main_type == 'text':
    fp = open(file, 'r')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  elif sub_type == 'pdf':
    fp = open(file, 'rb')
    msg = MIMEApplication(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def create_message(receiver_name, receiver_email, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = '{} <{}>'.format(receiver_name, receiver_email)
  message['from'] = 'Bored Apes Portfolio <boredapes.portfolio@gmail.com>'
  message['subject'] = subject
  message['reply-to'] = 'Bored Apes Portfolio <boredapes.portfolio@gmail.com>'
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def get_credentials():
    """
    Get the user's Gmail credentials
    """
    creds = None

    # Need to be global to be accessed by send message function
    global service

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    print("***********************************")

    print(os.getcwd())

    print("***********************************")

    if os.path.exists('gmail/token.json'):
        creds = Credentials.from_authorized_user_file(
            'gmail/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app/gmail/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('app/gmail/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

    except HttpError as error:
        # Handle errors from gmail API.
        print("An error occurred here: {}").format(error)


def send_email(receiver_name, receiver_email, subject, message_text):
    """Send an email
    Args:
      receiver_name: Name of the receiver.
      receiver_email: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
    Returns:
      None
    """
    # Get the credentials
    get_credentials()

    # Create the message
    message = create_message(
        receiver_name, receiver_email, subject, message_text)

    # Send the message
    send_message(service, "me", message)


def send_email_with_attachment(receiver_name, receiver_email, subject, message_text, file):
    """Send an email with attachment
    Args:
      receiver_name: Name of the receiver.
      receiver_email: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
      file: The path to the file to be attached.
    Returns:
      None
    """
    # Get the credentials
    get_credentials()

    # Create the message
    message = create_message_with_attachment(
        receiver_name, receiver_email, subject, message_text, file)

    # Send the message
    send_message(service, "me", message)



