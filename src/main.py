import publico_scraper
import googlecalendar

def handler(event, context):
    print("Starting...")
    releases = publico_scraper.get_publico_releases()
    googlecalendar.publish_to_calendar(releases)
