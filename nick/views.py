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
import json


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


def results(request):
    """This view is responsible for getting the data from the quiz and returning a number of recommendations
    Each question has a "TYPE" so we can identify which type of question is (and also enable the possibility of adding more)
    And we fork the queryset to each filter by identifying if the question is not set to a FALSE value
    """
    # Only via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=304)
    data = json.loads(request.body)
    queryset = Title.valid()

    # We union every genre filtered version of the queryset, then we intersect with the original queryset.
    if data["genre"]:
        initial_queryset = Title.objects.none()
        for genre in data["genre"]:
            qs = queryset.filter(genre__id=int(genre))
            initial_queryset |= qs

        queryset = queryset & initial_queryset
        queryset = queryset.distinct()

    # We filter by answer by only allowing movies release in the decades defined by the response.
    if data["decade"]:
        match data["decade"]:
            case "recent":
                queryset = queryset.filter(release_date__year__gte="2010")
            case "00s":
                queryset = queryset.filter(release_date__year__gte="2000").filter(
                    release_date__year__lt="2010"
                )
            case "90s":
                queryset = queryset.filter(release_date__year__gte="1990").filter(
                    release_date__year__lt="2000"
                )
            case "80s":
                queryset = queryset.filter(release_date__year__gte="1980").filter(
                    release_date__year__lt="1990"
                )
    # Filter by type of certification
    if data["certification"]:
        match data["certification"]:
            case "PG":
                queryset = queryset.filter(certification="PG")
            case "PG-13":
                queryset = queryset.filter(certification="PG-13")
            case "R":
                queryset = queryset.exclude(
                    Q(certification="PG-13") | Q(certification="PG")
                )
    # This one took a bit: we have to order by the number of matches of keywords in the answer list
    if data["keywords"]:
        queryset = queryset.annotate(
            num_matches=Count("keywords", filter=Q(keywords__pk__in=data["keywords"]))
        ).order_by("-num_matches")

    # If the user wants to order by popularity, we do it after ordering the keywords
    if data["popularity"]:
        queryset = queryset.order_by("-vote_average")
    
    # Now we get the serialized version of the queryset to send to the user, maybe restrict how many we send?
    serializer = TitleSerializer(queryset, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False, status=200)

class TitleViewSet(viewsets.ModelViewSet):
    """This view generates all valid titles as JSON, we use this to serialize all data used in the "result from quiz view"""
    queryset = Title.valid()
    serializer_class = TitleSerializer
    http_method_names = ["get"]
