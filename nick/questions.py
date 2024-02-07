from .models import *

questions = {
    "questions": [
        {
            "Title": "How are you today?",
            "Options": [('gif1', "gif1"), ('gif2', "gif2"), ('gif3', "gif3")],
            "Select": "img"
        },
        {
            "Title": "Choose any genre you're interested in",
            "Options": [(x.id, str(x)) for x in list(Genre.most_used())],
            "Select": "or"
        },
        {
            "Title": "Do you wish the movie to be from a specific decade?",
            "Options": [
                (False, "Doesn't matter"),
                ("recent", "2010's and 2020s"),
                ("00s", "2000's"),
                ("90s", "1990's"),
                ("80s","1980's"),
            ],
            "Select": "and",
        },
        {
            "Title": "Do you wish to select prefered age ratings?",
            "Options": [
                (False, "Doesn't matter"),
                ("PG", "Older kids 7+ (PG)"),
                ("PG-13", "Teens 13+ (PG-13)"),
                ("R", "Adults 18+ (NC-17, NR, R and Unrated)")
            ],
            "Select": "and"
        },
        {
            "Title": "Select any other keyword you're interested in.",
            "Options": [(False, "Doesn't matter")] + [(x.id, f"'{str(x).title()}'") for x in list(Keyword.most_used())],
            "Select": "or"
        },
    ]
}
