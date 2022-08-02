from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import pprint

months = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez"
]

releases_endpoint = '/Brevemente'
url = 'https://cinecartaz.publico.pt'


def get_publico_releases():
    # Fetch web page
    page = urlopen(url + releases_endpoint).read()
    soup = BeautifulSoup(page, 'html.parser')
    boxes = soup.find_all(class_="box")

    # Build list of release dates
    result_obj = []
    for box in boxes:
        title_span = box.find(class_="boxtitle")
        title= title_span.text
        title = title.split(" ")
        day = title[4]
        month = title[6]
        month_number = months.index(month) + 1
        year = title[8]

        date = datetime.date(int(year), month_number, int(day))
        date_iso_format = date.isoformat()

        day_releases = {
            "date": date_iso_format,
            "movies": []
        }

        movies = box.find_all(class_="blocklink")
        for movie in movies:
            # Get original movie title
            movie_url = url + movie["href"]
            movie_page = urlopen(movie_url).read()
            movie_soup = BeautifulSoup(movie_page, 'html.parser')

            movie_title = movie_soup.find("dd").text
            day_releases['movies'].append(movie_title)
        result_obj.append(day_releases)
    return result_obj

if __name__ == '__main__':
    releases = get_publico_releases()
    pprint.pprint(releases)
