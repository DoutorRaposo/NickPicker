from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

def index(request):
    return render(request, "nick/index.html")


def get_movies(request, genre=None):
    if genre == None:
        queryset = Title.valid()
        title = "Movies by Cage"

    else:
        genre_model = Genre.valid().get(name__icontains=genre)
        queryset = Title.valid().filter(genre__id=genre_model.id)
        title = genre_model.name

    return render(request, "nick/movies_set.html", context={"movies": queryset, "title": title})


def get_title(request, id):
    movie = Title.objects.get(pk=id)
    return render(request, "nick/title.html", context={"movie": movie})


def search(request):
    query = request.GET.get("q", "")
    queryset = Title.valid().filter(
        Q(title__icontains=query)
        | Q(genre__name__icontains=query)
        | Q(keywords__name__icontains=query)
        | Q(overview__icontains=query)
        | Q(tagline__icontains=query)
        | Q(director__name__icontains=query)
        | Q(character__icontains=query)
        | Q(cast_members__icontains=query)
    )
    queryset = queryset.distinct()
    return render(request, "nick/movies_set.html", context={"movies": queryset, "title": f'Results for "{query}"'})

# Install CORS?

# This viewset is for the API to return all the valid titles at /api/titles
# Valid titles are Released titles that are Movies with Nic Cage as an Actor
# Another viewser maybe will be required for the Trivia Section
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ["get"]


# We have to create separate jsons for the serializer url to work?
class TitleValidViewSet(viewsets.ModelViewSet):
    queryset = Title.valid()
    serializer_class = TitleSerializer
    http_method_names = ["get"]


# Ambas funcionam, mas qual usar? talvez a função use para search.
def title_list(request):
    queryset = Title.valid()
    serializer = TitleSerializer(queryset, many=True, context={"request": request})
    print(request.GET.get("q", "teste"))
    return JsonResponse(serializer.data, safe=False)
