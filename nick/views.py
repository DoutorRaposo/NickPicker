from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

from django.http import HttpResponse, JsonResponse

# Install CORS?

# Create your views here.
def index(request):
    return render(request, "nick/index.html")

# This viewset is for the API to return all the valid titles at /api/titles
# Valid titles are Released titles that are Movies with Nic Cage as an Actor
# Another viewser maybe will be required for the Trivia Section
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    http_method_names = ['get']
# We have to create separate jsons for the serializer url to work?
class TitleValidViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().filter(media_type="MV").filter(role_type="Cast").filter(status="Released").filter(vote_average__gte=2.1).order_by("-release_date")
    serializer_class = TitleSerializer
    http_method_names = ['get']

# Ambas funcionam, mas qual usar? talvez a função use para search.
def title_list(request):
    queryset = Title.objects.all().filter(media_type="MV").filter(role_type="Cast").filter(status="Released").filter(vote_average__gte=2.1).order_by("-release_date")
    serializer = TitleSerializer(queryset, many=True, context={'request': request})
    print(request.GET.get('q', 'teste'))
    return JsonResponse(serializer.data, safe=False)