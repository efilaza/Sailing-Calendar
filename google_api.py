import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError


class Google_Api:

    def __init__(self, district):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        CLIENT_SECRET = 'json/client_secret.json'
        API_NAME = 'Calendar'
        VERSION = 'v3'
        creds = None
        if os.path.exists('storage.json'):
            creds = Credentials.from_authorized_user_file('storage.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('storage.json', 'w') as token:
                token.write(creds.to_json())
        try:
            self.service = build(API_NAME, VERSION, credentials=creds)

            request_body = {
                'summary': district
            }
            # Δημιουργία ημερολογίου
            self.service.calendars().insert(body=request_body).execute()
            response = self.service.calendarList().list().execute()
            calendarItems = response.get('items')
            self.myCalendar = filter(lambda x: district in x['summary'], calendarItems)
            self.myCalendar = next(self.myCalendar)
        except HttpError as error:
            print(error)
            print("Σφάλμα σύνδεσης.")

    def insert_event(self, event):
        # Create event ()
        self.service.events().insert(calendarId=self.myCalendar['id'], body=event).execute()
