import json
from nick.models import *

def script():
    with open("genres_movie.json") as file:
        data = json.load(file)
        for genre in data["genres"]:
            Genre.objects.create(name=genre['name'], tmdb_id=genre['id'])