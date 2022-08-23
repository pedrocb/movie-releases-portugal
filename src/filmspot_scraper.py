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

def get_movie_releases():
    releases = []

    # Fetch web page
    page = urlopen("https://filmspot.pt/estreias")
    soup = BeautifulSoup(page, 'html.parser')

    release_date_sections = soup.find_all(class_="estreiasH2")
    for release_date_section in release_date_sections:
        date_text = release_date_section.text
        date_text_split = date_text.split(" ")
        day = date_text_split[0]
        month = date_text_split[2]
        month_number = months.index(month) + 1
        year = date_text_split[4]
        date = datetime.date(int(year), month_number, int(day))

        movies = release_date_section.next_sibling.find_all(class_="filmeLista")
        for movie in movies:
            movie_title_spans = movie.find_all("span")
            movie_title = movie_title_spans[0].text if len(movie_title_spans) == 1 else movie_title_spans[1].text
            movie_data = {
                "title": movie_title,
                "date": date.isoformat(),
                "description": str(movie.find(class_="filmeListaInfo"))
            }
            releases.append(movie_data)

    return releases

if __name__ == "__main__":
    pprint.pprint(get_movie_releases())
