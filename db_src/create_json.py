import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_API_KEY}"}


def generate():
    nic_id = 2963
    urls = {
        "genres_movie": "https://api.themoviedb.org/3/genre/movie/list?language=en",
        "genres_tv": "https://api.themoviedb.org/3/genre/tv/list?language=en",
        "combined": "https://api.themoviedb.org/3/person/"
        + str(nic_id)
        + "?append_to_response=combined_credits&language=en-US",
    }

    for filename, url in urls.items():
        data = get_data(url)
        if filename == "combined":
            for _, titles in data["combined_credits"].items():
                for title in titles:
                    add_info(title)
        write_json(filename, data)
        print(f"{filename}.json written.")


def get_data(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def write_json(filename, data):
    with open(f"db_src/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


def add_info(title):
    id = title["id"]
    if title["media_type"] == "movie":
        url = f"https://api.themoviedb.org/3/movie/{id}?append_to_response=keywords%2Ccredits%2Crelease_dates&language=en-US"
        data = get_data(url)
        title["budget"] = data["budget"]
        title["revenue"] = data["revenue"]
        title["runtime"] = data["runtime"]
        title["status"] = data["status"]
        title["keywords"] = data["keywords"]
        title["production_companies"] = data["production_companies"]
        title["tagline"] = data["tagline"]
        title["credits"] = data["credits"]
        title["release_dates"] = data["release_dates"]
        print(f'Extra info added for "{title["title"]}".')
    if title["media_type"] == "tv":
        url = f"https://api.themoviedb.org/3/tv/{id}?append_to_response=keywords&language=en-US"
        data = get_data(url)
        title["in_production"] = data["in_production"]
        title["status"] = data["status"]
        title["tagline"] = data["tagline"]
        title["keywords"] = data["keywords"]
        print(f'Extra info added for "{title["name"]}".')
