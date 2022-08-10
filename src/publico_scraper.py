from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import pprint

months = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "dezembro"
]

releases_endpoint = '/em-breve'
url = 'https://cinecartaz.publico.pt'


def get_publico_releases():
    # Fetch web page
    page = urlopen(url + releases_endpoint).read()
    soup = BeautifulSoup(page, 'html.parser')

    # Split release day sections
    release_date_sections = soup.find_all(class_="collection")

    # Build list of release dates
    releases = []
    for release_date_section in release_date_sections:
        # Convert date text to datetime date
        date_header = release_date_section.find(class_="collection__title")
        date_text = date_header.text
        date_text_split = date_text.split(" ")
        day = date_text_split[-3]
        month = date_text_split[-1]
        month_number = months.index(month) + 1
        # TODO: Logic for new year
        year = datetime.date.today().year

        date = datetime.date(int(year), month_number, int(day))
        date_iso_format = date.isoformat()

        day_releases = {
            "date": date_iso_format,
            "movies": []
        }

        movies = release_date_section.find_all(class_="block-link")
        for movie in movies:
            # Get original movie title
            movie_url = url + movie["href"]
            movie_page = urlopen(movie_url).read()
            movie_soup = BeautifulSoup(movie_page, 'html.parser')

            movie_title = movie_soup.find_all("div", class_="boxed")[0].text.strip()
            releases.append({
                "date": date_iso_format,
                "title": movie_title
            })
    return releases

if __name__ == '__main__':
    releases = get_publico_releases()
    pprint.pprint(releases)
