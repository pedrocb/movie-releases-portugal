import publico_scraper
import googlecalendar

if __name__ == '__main__':
    releases = publico_scraper.get_publico_releases()
    googlecalendar.publish_to_calendar(releases)
