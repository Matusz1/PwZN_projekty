import argparse
import requests
import json
from bs4 import BeautifulSoup

# Parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Filename to output movies')
args = parser.parse_args()

def load_movies_lvl_4():
    # Poziom 4:
    # Dodać nagłówki
    url = 'https://profmrow.fans/pwzn/toc4/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.find('select', class_ = 'form-control')

    movies = {}
    for year in form.find_all('option'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }
        data = {
            'year': year.text
        }
        res = requests.post(url, data=data, headers=headers)

        form_soup = BeautifulSoup(res.text, 'html.parser')
        movie_divs = form_soup.find_all('div', class_ = 'text-center mb-2')
        movies[int(year.text)] = [movie.text for movie in movie_divs]

    return movies

movies = load_movies_lvl_4()
json.dump(movies, open(args.filename, 'w'), indent=4)
