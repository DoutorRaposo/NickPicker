from .models import *

questions = {
    "questions": [
        {
            "Title": "How are you today?",
            "Options": ["gif1", "gif2", "gif3"],
            "Select": "img"
        },
        {
            "Title": "Choose any genre you're interested in",
            "Options": [str(x) for x in list(Genre.most_used())],
            "Select": "or"
        },
        {
            "Title": "Do you wish the movie to be from a specific decade?",
            "Options": [
                "Doesn't matter",
                "2010's and 2020s",
                "2000's",
                "1990's",
                "1980's",
            ],
            "Select": "and",
        },
        {
            "Title": "Do you wish to select prefered age ratings?",
            "Options": [
                "Doesn't matter",
                "Older kids 7+ (PG)",
                "Teens 13+ (PG-13)",
                "Adults 18+ (NC-17, NR, R and Unrated)",
            ],
            "Select": "and"
        },
        {
            "Title": "Select any other category you're interested in.",
            "Options": [
                "Doesn't matter",
                "Based on a novel or book",
                "Based on a true story",
                "Based on a comic",
                "Movies in New York",
                "Movies about revenge or murder",
                "Dark Comedies",
                "Movies with high voter score",
                "Docs with Nick Cage",
            ],
            "Select": "or"
        },
    ]
}
