from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.modify']


def scarpe():
    """
    Returns all unread emails
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
        messages = results.get('messages', [])
        all_msg_data = {}

        for message in messages:
            one_msg_data = []
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            payload = msg['payload']
            headers = payload['headers']
            for d in headers:
                if d['name'] == 'Date':
                    date = d['value']

                if d['name'] == 'From':
                    sender = d['value']

                if d['name'] == 'Subject':
                    subject = d['value']

            mail_body = msg['snippet'].split('For more information visit')[0] # for my purpose - I don't need all content of email

            mail_key = subject

            one_msg_data.append(date)
            one_msg_data.append(sender)
            one_msg_data.append(subject)
            one_msg_data.append(msg['snippet'])

            all_msg_data[mail_key] = one_msg_data

            service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

        return all_msg_data

    except HttpError as error:
        print(f'An error occurred: {error}')
