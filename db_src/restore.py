import json
import datetime
from nick.models import *


def restore_db():
    Genre.objects.all().delete()
    Title.objects.all().delete()
    Keyword.objects.all().delete()
    Company.objects.all().delete()
    Director.objects.all().delete()
    print("Database cleared")

    subscript_genres()
    print("Genres added")
    subscript_add_info()
    print("Additional info added.")
    subscript_titles()
    print("Titles added")


def subscript_genres():
    with open("db_src/genres_movie.json") as file:
        data_movies = json.load(file)
    with open("db_src/genres_tv.json") as file:
        data_tv = json.load(file)
    data_movies = data_movies["genres"]
    data_tv = data_tv["genres"]
    for item in data_tv:
        if item not in data_movies:
            data_movies.append(item)
    for genre in data_movies:
        Genre.objects.create(name=genre["name"], tmdb_id=genre["id"])

def subscript_add_info():
    with open("db_src/combined.json") as file:
        data_keywords = json.load(file)

    for role in data_keywords['combined_credits']:
        for title in data_keywords['combined_credits'][role]:
            if "production_companies" in title:
                companies_list = list(title["production_companies"])
                for company in companies_list:
                    if not Company.objects.filter(tmdb_id=company["id"]).exists():
                        Company.objects.create(tmdb_id=company['id'], name=company['name'])

            keyword_list = list(title['keywords'].values())
            if keyword_list[0]:
                for keyword in keyword_list[0]:
                    if not Keyword.objects.filter(tmdb_id=keyword["id"]).exists():
                        Keyword.objects.create(tmdb_id=keyword['id'], name=keyword['name'])
            if title['media_type'] == "movie":
                if "crew" in title['credits']:
                    for crewmember in title['credits']['crew']:
                        if "job" in crewmember:
                            if crewmember['job'] == "Director":
                                if not Director.objects.filter(tmdb_id=crewmember["id"]).exists():
                                    Director.objects.create(tmdb_id=crewmember['id'], name=crewmember['name']) 
                            

def subscript_titles():
    with open("db_src/combined.json") as file:
        data = json.load(file)

    credits = data["combined_credits"]

    for role in credits:
        for title in credits[role]:
            date = get_date(title)
            tmdb_id = title["id"]
            media_type = title["media_type"]
            if media_type == "tv":
                original_title = title["name"]
                media_type = "TV"
            elif media_type == "movie":
                original_title = title["title"]
                media_type = "MV"

            overview = title["overview"]
            genres = title["genre_ids"]
            if role == "cast":
                obj_role = "Actor"
                character = title["character"]
            elif role == "crew":
                obj_role = title["job"]
                character = ""

            if title["poster_path"]:
                poster_path = (
                    "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
                    + title["poster_path"]
                )
            else:
                poster_path = ""

            object = Title.objects.create(
                title=original_title,
                overview=overview,
                tmdb_id=tmdb_id,
                role=obj_role,
                character=character,
                media_type=media_type,
            )

            if media_type == "MV":
                object.budget = title["budget"]
                object.revenue = title['revenue']
                object.runtime = title['runtime']
                object.status = title['status']
                object.tagline = title['tagline']
                for keyword in title['keywords']['keywords']:
                    object.keywords.add(Keyword.objects.get(tmdb_id=keyword['id']))
                for company in title['production_companies']:
                    object.companies.add(Company.objects.get(tmdb_id=company['id']))
                for crewmember in title['credits']['crew']:
                    if crewmember['job'] == "Director":
                        object.director.add(Director.objects.get(tmdb_id=crewmember['id']))
                for item in title['release_dates']['results']:
                    if item["iso_3166_1"] == "US":
                        certification = item["release_dates"][0]['certification']
                        object.certification = certification
            if date != "":
                object.release_date = date
            if poster_path != "":
                object.poster_path = poster_path
            for genre_id in genres:
                genre = Genre.objects.filter(tmdb_id=genre_id).first()
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
        date = datetime.date(*map(int, release_list))
    else:
        date = ""

    return date
