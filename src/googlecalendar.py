from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import base64
import boto3
import json
import os.path
import pdb

SERVICE_ACCOUNT_FILE = 'client_secret.json'
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "h7s9ktaog3hm0bofal9hurvpic@group.calendar.google.com"

def calendar_service():
    if not os.path.isfile('client_secret.json'):
        client = boto3.client('secretsmanager', region_name='eu-west-1')

        response = client.get_secret_value(
            SecretId='movie-releases-gcp'
        )
        creds = service_account.Credentials.from_service_account_info(
            json.loads(response['SecretString']), scopes=SCOPES
        )
    else:
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
            if 'source' in event:
                created_events[event['source']['title']] = True
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    print("Got Events")

    for release in releases:
        if release["title"] not in created_events.keys():
            release_datetime = datetime.date.fromisoformat(release['date'])
            event = {
                'summary': release["title"],
                'description': release["description"],
                'source': {
                    'title': release["title"],
                    'url': "https://placeholder"
                },
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
            print("Inserted {}".format(release["title"]))

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
