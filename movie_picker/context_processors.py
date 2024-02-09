from nick.models import Genre


def genre_template(request):
    """This context processor is used to generate the list of genres that can be used in the dropdown menu"""
    return {
        'genres': Genre.valid(),
    }