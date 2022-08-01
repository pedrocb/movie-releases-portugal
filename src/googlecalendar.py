from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import publico_scraper
import pdb


SERVICE_ACCOUNT_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "h7s9ktaog3hm0bofal9hurvpic@group.calendar.google.com"

def publish_to_calendar(releases):
    creds = service_account.Credentials.from_service_account_file(
        'client_secret.json', scopes=SCOPES
    )

    try:
        service = build('calendar', 'v3', credentials=creds)
        for release_date in releases:
            release_datetime = datetime.date.fromisoformat(release_date['date'])
            for movie in release_date["movies"]:
                event = {
                    'summary': movie,
                    'start': {
                        'date': release_datetime.isoformat(),
                        'timeZone': 'Europe/Lisbon'
                    },
                    'end': {
                        'date': release_datetime.isoformat(),
                        'timeZone': 'Europe/Lisbon'
                    }
                }

    except HttpError as error:
        print('An error occurred: %s' % error)
