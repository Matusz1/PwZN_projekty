import argparse
import requests
import json
from bs4 import BeautifulSoup

# Parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Filename to output movies')
args = parser.parse_args()

def load_movies_lvl_1():
    # Poziom 1:
    # Wystarczy wpisywać rok w adresie URL
    url = 'https://profmrow.fans/pwzn/toc1/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    form = soup.find('select', class_ = 'form-control')

    movies = {}
    for year in form.find_all('option'):
        year_url = url + f'?year={year.text}'
        year_soup = BeautifulSoup(requests.get(year_url).text, 'html.parser')
        movie_divs = year_soup.find_all('div', class_ = 'text-center mb-2')
        movies[int(year.text)] = [movie.text for movie in movie_divs]

    return movies

movies = load_movies_lvl_1()
json.dump(movies, open(args.filename, 'w'), indent=4)
