import pandas as pd 
from imdb import Cinemagoer
import json
import warnings
warnings.filterwarnings('ignore')
ia = Cinemagoer()
movie = ia.get_movie('0133093')
movie_data_ =  {
    "imdbID" : movie['imdbID'],
    "original title": movie["original title"],
    "genres": ",".join(movie['genres']) if isinstance(movie['genres'], list) else movie['genres'],
    "countries": ",".join(movie["countries"])if isinstance(movie['countries'], list) else movie['countries'],
    "country codes": ",".join(movie["country codes"]) if isinstance(movie['country codes'], list) else movie['country codes'],
    "box office": movie['box office']["Budget"],
    "certificates": movie['certificates'][17],
    "rating": movie["rating"],
    "votes": movie["votes"],
    "plot outline": movie['plot outline'],
    "year": movie["year"],
    "kind": movie["kind"],
    "full-size cover url": movie['full-size cover url']
  }
df = pd.DataFrame(movie_data_, index=[movie_data_["imdbID"]])
df.drop("imdbID",axis=1, inplace=True)
numbers = [str(i).zfill(7) for i in range(1, 100)]


for i in numbers:
      try:
        movie = ia.get_movie(i)
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
          movie_data["certificates"] =  rating
        except:
          movie_data["certificates"] =  "N/A"

        df_to_append = pd.DataFrame(movie_data, index=[movie_data["imdbID"]])
        df_to_append.drop("imdbID",axis=1, inplace=True)
        df = df.append(df_to_append)
        print(f"{movie_data['original title']} crawled")
        
      except Exception as e:
          print(e)
          print(f"Not possible for {i}")