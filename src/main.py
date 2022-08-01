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
import googlecalendar
import pdb


if __name__ == '__main__':
    releases = publico_scraper.get_publico_releases()
    googlecalendar.publish_to_calendar(releases)
