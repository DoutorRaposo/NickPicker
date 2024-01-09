import json
from nick.models import *

def script():
    with open("genres_movie.json") as file:
        data_movies = json.load(file)
    with open("genres_tv.json") as file:
        data_tv = json.load(file)
    data_movies = data_movies['genres']
    data_tv = data_tv['genres']
    new_dict = {}
    for item in data_tv:
        if item not in data_movies:
            data_movies.append(item)
    for genre in data_movies:
        Genre.objects.create(name=genre['name'], tmdb_id=genre['id'])