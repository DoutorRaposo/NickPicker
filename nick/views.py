from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
def index(request):
    return render(request, "nick/index.html")

# This viewset is for the API to return all the valid titles at /api/titles
# Valid titles are Released titles that are Movies with Nic Cage as an Actor
# Another viewser maybe will be required for the Trivia Section
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().filter(media_type="MV").filter(role__startswith="Actor").filter(status="Released").filter(vote_average__gte=2.1).order_by("-release_date")
    serializer_class = TitleSerializer
    http_method_names = ['get']