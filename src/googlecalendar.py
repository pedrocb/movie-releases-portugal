from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import pdb


SERVICE_ACCOUNT_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "h7s9ktaog3hm0bofal9hurvpic@group.calendar.google.com"

def calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        'client_secret.json', scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)
    return service

def publish_to_calendar(releases):
    service = calendar_service()
    page_token = None
    created_events =  {}
    while True:
        events = service.events().list(calendarId=CALENDAR_ID, pageToken=page_token).execute()
        for event in events['items']:
            created_events[event['summary']] = True
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    print("Got Events")

    for release_date in releases:
        release_datetime = datetime.date.fromisoformat(release_date['date'])
        for movie in release_date["movies"]:
            if movie not in created_events.keys():
                print("Inserted {}".format(movie))
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

def clear_calendar():
    service = calendar_service()
    page_token = None
    while True:
        events = service.events().list(calendarId=CALENDAR_ID, pageToken=page_token).execute()
        for event in events['items']:
            service.events().delete(calendarId=CALENDAR_ID, eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break
