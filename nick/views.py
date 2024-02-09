from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
import random
from django.shortcuts import redirect
from django.core.paginator import Paginator
from .questions import questions


def index(request):
    """Default index view"""
    return render(request, "nick/index.html")


def get_movies(request, genre=None):
    """This view enables us to render all titles either by no filter or by genre filter
    Pagination for the titles can be altered here"""
    if genre == None:
        queryset = Title.valid()
        title = "Movies by Cage"

    else:
        genre_model = get_object_or_404(Genre.valid(), name__icontains=genre)
        queryset = Title.valid().filter(genre__id=genre_model.id)
        title = genre_model.name

    paginator = Paginator(queryset, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "nick/movies_set.html", context={"movies": page_obj, "title": title}
    )


def get_title(request, id):
    """Single movie page"""
    movie = Title.objects.get(pk=id)
    return render(request, "nick/title.html", context={"movie": movie})


def random_title(request):
    """Redirects to random single movie page!"""
    titles = list(Title.valid())
    random_title = random.choice(titles)
    return redirect("get_single_movie", id=random_title.id)


def search(request):
    """Searches using every useful item in the model, not only the title name"""
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
    return render(
        request,
        "nick/movies_set.html",
        context={"movies": queryset, "title": f'Results for "{query}"'},
    )

def get_questions(request):
    """This serves as an API response to the JS on the front-end to get all questions"""
    return JsonResponse(questions, safe=False)


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
