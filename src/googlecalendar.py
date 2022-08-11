from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import pdb
import boto3
import os.path

SERVICE_ACCOUNT_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "h7s9ktaog3hm0bofal9hurvpic@group.calendar.google.com"

def calendar_service():
    if not os.path.isfile('client_secret.json'):
        client = boto3.client('secretsmanager', region_name='eu-west-1')

        response = client.get_secret_value(
            SecretId='movie-releases-gcp'
        )
        with open('client_secret.json', "w") as fd:
            fd.write(response['SecretString'])


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

    for release in releases:
        if release["title"] not in created_events.keys():
            release_datetime = datetime.date.fromisoformat(release['date'])
            print("Inserted {}".format(release["title"]))
            event = {
                'summary': release["title"],
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
