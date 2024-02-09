from .models import *

"""This module is responsible for all questions that will be displayed in the quiz section
There can be three types: 'img' (for image based questions), 'xor' (for exclusive choice questions) and 'and' (for multiple choice questions)
Further implementation is on the view responsible for processing this data, but generally if the question correlates with a model we'll use the ID as the value for checking the results.
If there's no direct correlation with the models, I'm using a string to identify the answer."""

questions = {
    "questions": [
        {
            "Title": "How are you today?",
            # first value should indicate the description of the image
            "Options": [
                ("Hysterical", "/static/nick/images/hysterical.gif"),
                ("Happy", "/static/nick/images/happy.gif"),
                ("Crazy", "/static/nick/images/crazy.gif"),
                ("Sad", "/static/nick/images/sad.gif"),
            ],
            "Select": "img",
        },
        {
            "Title": "Choose any genre you're interested in",
            "Options": [(False, "Any genre")]
            + [(x.id, str(x)) for x in list(Genre.most_used())],
            "Select": "and",
        },
        {
            "Title": "Do you wish the movie to be from a specific decade?",
            "Options": [
                (False, "Any decade"),
                ("recent", "2010's and 2020s"),
                ("00s", "2000's"),
                ("90s", "1990's"),
                ("80s", "1980's"),
            ],
            "Select": "xor",
        },
        {
            "Title": "Do you wish to select prefered age ratings?",
            "Options": [
                (False, "No prefered age rating"),
                ("PG", "Older kids 7+ (PG)"),
                ("PG-13", "Teens 13+ (PG-13)"),
                ("R", "Adults 18+ (NC-17, NR, R and Unrated)"),
            ],
            "Select": "xor",
        },
        {
            "Title": "Do you care about movie popularity?",
            "Options": [
                (False, "No, I don't mind"),
                (True, "Yes, I care about user votes and movie popularity"),
            ],
            "Select": "xor",
        },
        {
            "Title": "Select any other keyword you're interested in.",
            "Options": [(False, "No other keyword")]
            + [(x.id, f"'{str(x).title()}'") for x in list(Keyword.most_used())],
            "Select": "and",
        },
    ]
}
