from nick.models import Genre

def genre_template(request):
    return {
        'genres': Genre.valid(),
    }