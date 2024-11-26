import argparse
import requests
import json
from bs4 import BeautifulSoup

# Parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Filename to output movies')
args = parser.parse_args()

def load_movies_lvl_2():
    # Poziom 2:
    # Wystarczy wysłać dane formularza POST
    url = 'https://profmrow.fans/pwzn/toc2/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    form = soup.find('select', class_ = 'form-control')

    movies = {}
    for year in form.find_all('option'):
        data = {
            'year': year.text
        }
        res = requests.post(url, data = data)
        form_soup = BeautifulSoup(res.text, 'html.parser')
        movie_divs = form_soup.find_all('div', class_ = 'text-center mb-2')
        movies[int(year.text)] = [movie.text for movie in movie_divs]

    return movies

movies = load_movies_lvl_2()
json.dump(movies, open(args.filename, 'w'), indent=4)
