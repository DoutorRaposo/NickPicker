import json
from nick.models import *


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

