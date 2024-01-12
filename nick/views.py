from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
def index(request):
    return render(request, "nick/index.html")

class TitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Title.objects.all().filter(media_type="MV").filter(role="Actor").filter(status="Released").order_by("-release_date")
    serializer_class = TitleSerializer
    http_method_names = ['get']