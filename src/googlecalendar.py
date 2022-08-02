from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError


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
                service.events().insert(calendarId=CALENDAR_ID, body=event).execute()


    except HttpError as error:
        print('An error occurred: %s' % error)

def clear_calendar():
    creds = service_account.Credentials.from_service_account_file(
        'client_secret.json', scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)
    page_token = None
    while True:
        events = service.events().list(calendarId=CALENDAR_ID, pageToken=page_token).execute()
        for event in events['items']:
            service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break
