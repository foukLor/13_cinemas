import requests
from bs4 import BeautifulSoup
import random

AFISHA_URL = "http://www.afisha.ru/msk/schedule_cinema/"
KINOPOISK_URL = "https://www.kinopoisk.ru/index.php"
TIMEOUT = 10

def fetch_afisha_page():
    return requests.get(AFISHA_URL).content


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    movies_info = soup.find_all('div', {'class': 'object'})
    movies = []
    for movie_div in movies_info:
        title = movie_div.find('h3', {'class': 'usetags'}).text
        count_cinemas = len(movie_div.find_all("td",
                                attrs={"class": "b-td-item"}))
        rating, count_ratings = get_movie_raiting(title)
        movies.append({ 'title'          : title,
                        'num_of_cinemas' : count_cinemas,
                        'rating'        : rating,
                        'count_ratings' : count_ratings
            })
    return movies




def fetch_movie_info(movie_title):
    payload = {'first': 'yes', "kp_query": movie_title}
    headers = { 'Accept-Encoding': 'UTF-8',
                'Accept-Language': 'Ru-ru',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'\
                            ' Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36'
                                            }
    kinopoisk_page = requests.get(KINOPOISK_URL, params = payload, headers=headers, timeout=TIMEOUT).content
    return kinopoisk_page

def get_movie_raiting(movie_title):  
    kinopoisk_page = fetch_movie_info(movie_title)
    soup = BeautifulSoup(kinopoisk_page, 'html.parser')
    movie_rating_html = soup.find('span', {'class': 'rating_ball'})
    if movie_rating_html:
        movie_rating = float(movie_rating_html.text)
    else:
        movie_rating = 0
    num_of_votes_html_tag = soup.find('span', {'class': 'ratingCount'})
    if num_of_votes_html_tag:
        num_of_votes = int(''.join(num_of_votes_html_tag.text.split()))
    else:
        num_of_votes = 0
    return movie_rating, num_of_votes



def output_movies_to_console(movies, count=10):
    print('title  count cinemas  rating  count ratings')
    movies = sorted(movies, key=lambda movie: movie['rating'], reverse=True)
    for movie in movies[:count]:
        print('{0}  {1}  {2}  {3}'.format(movie['title'],
                                     movie['num_of_cinemas'],
                                     movie['rating'],
                                     movie['count_ratings']))
    return

if __name__ == '__main__':
    afisha_page = fetch_afisha_page()
    movies = parse_afisha_list(afisha_page)
    output_movies_to_console(movies)

