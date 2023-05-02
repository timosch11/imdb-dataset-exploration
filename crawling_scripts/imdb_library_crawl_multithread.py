import pandas as pd
from imdb import Cinemagoer
import json
import warnings
import concurrent.futures
import time
from ratelimit import limits, sleep_and_retry


_from = 40001  #IMDBID to start with
_to = 40050   #IMDBID to end with
warnings.filterwarnings('ignore')
ia = Cinemagoer()

numbers = [str(i).zfill(7) for i in range(_from, _to)]
results = []
counter = 0
@sleep_and_retry
def crawl_movie_data(number):
    try:
        movie = ia.get_movie(number)
        movie_data = {
            "imdbID": movie.get('imdbID', 'N/A'),
            "original title": movie.get("original title", 'N/A'),
            "genres": ",".join(movie.get('genres', [])) if isinstance(movie.get('genres', []), list) else movie.get('genres', 'N/A'),
            "countries": ",".join(movie.get("countries", [])) if isinstance(movie.get('countries', []), list) else movie.get('countries', 'N/A'),
            "country codes": ",".join(movie.get("country codes", [])) if isinstance(movie.get('country codes', []), list) else movie.get('country codes', 'N/A'),
            "box office": movie.get("box office", {}).get("Budget", "N/A"),
            "certificates": "N/A",
            "rating": movie.get("rating", 'N/A'),
            "votes": movie.get("votes", 'N/A'),
            "plot outline": movie.get('plot outline', 'N/A'),
            "year": movie.get("year", 'N/A'),
            "kind": movie.get("kind", 'N/A'),
            "full-size cover url": movie.get('full-size cover url', 'N/A')
        }
        try:
            for entry in movie['certificates']:
                if 'germany' in entry.lower():
                    rating = entry
                    break
            movie_data["certificates"] = rating
        except:
            movie_data["certificates"] = "N/A"
        
        return movie_data

    except Exception as e:
        return None

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_number = {executor.submit(crawl_movie_data, number): number for number in numbers}
    for future in concurrent.futures.as_completed(future_to_number):
        number = future_to_number[future]
        result = future.result()
        if result:
            results.append(result)
            print(f"{result['original title']} crawled")
            counter += 1
        if counter % 1000 == 0:
            print("Sleep 60 sec to avoid getting banned")

df = pd.DataFrame(results)
df.set_index("imdbID", inplace=True)


df.to_csv(f"crawling_scripts/crawlings/imdb_crawl{_from}_{_to}.csv")

