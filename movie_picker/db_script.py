import json
import datetime
from nick.models import *

def run():
    subscript_genres()
    print("Genres added")
    subscript_titles()
    print("Titles added")
    


def subscript_genres():
    with open("scripts_json/genres_movie.json") as file:
        data_movies = json.load(file)
    with open("scripts_json/genres_tv.json") as file:
        data_tv = json.load(file)
    data_movies = data_movies['genres']
    data_tv = data_tv['genres']
    new_dict = {}
    for item in data_tv:
        if item not in data_movies:
            data_movies.append(item)
    for genre in data_movies:
        Genre.objects.create(name=genre['name'], tmdb_id=genre['id'])

def subscript_titles():
    with open("scripts_json/nic_cage_combined.json") as file:
        data = json.load(file)

    credits = data["combined_credits"]

    for role in credits:
        for title in credits[role]:
            date = get_date(title)
            tmdb_id = title['id']
            media_type = title['media_type']
            if media_type == 'tv':
                original_title = title['name']
                media_type = "TV"
            else:
                original_title = title['title']
                media_type = "MV"
            overview = title['overview']
            genres = title['genre_ids']
            if role == "cast":
                obj_role = title['character']
                credit_type = "ACT"
            else:
                obj_role = title['job']
                credit_type = "CRW"
            
            if title['poster_path']:
                poster_path = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2" + title['poster_path']
            else:
                poster_path = ''

            object = Title.objects.create(title=original_title, overview=overview, tmdb_id=tmdb_id, role=obj_role, media_type=media_type,credit_type=credit_type)
            if date != '':
                object.release_date =  date
            if poster_path != "":
                object.poster_path = poster_path
            for genre_id in genres:
                genre = Genre.objects.get(tmdb_id=genre_id)
                object.genre.add(genre)
            object.save()



def get_date(title):
    match title["media_type"]:
        case "movie":
            release_str = title["release_date"]

        case "tv":
            release_str = title["first_air_date"]

    release_list = release_str.split("-")
    if release_list != [""]:
        date = datetime.datetime(*map(int, release_list))
    else:
        date = ""

    return date