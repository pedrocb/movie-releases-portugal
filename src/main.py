import filmspot_scraper
import googlecalendar

def handler(event, context):
    print("Starting...")
    releases = filmspot_scraper.get_movie_releases()
    googlecalendar.publish_to_calendar(releases)
