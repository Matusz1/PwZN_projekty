import argparse
import requests
import json
# from bs4 import BeautifulSoup

# Parse the input arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='Filename to output movies')
args = parser.parse_args()

def load_movies_lvl_5():
    # Poziom 5:
    # Bespośrednio zczytaj dane
    # url = 'https://profmrow.fans/pwzn/toc5/'
    url = 'https://profmrow.fans/pwzn/chuck_service/?mode=years'
    res = requests.get(url)
    res = json.loads(res.text)

    movies = {}
    for year in res:
        url = 'https://profmrow.fans/pwzn/chuck_service/?mode=year&year=' + year
        res = json.loads(requests.get(url).text)

        movies[int(year)] = [movie['title'] for movie in res]

    return movies

movies = load_movies_lvl_5()
json.dump(movies, open(args.filename, 'w'), indent=4)
