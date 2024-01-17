from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/titles", views.TitleViewSet)
router.register(r"api/titles-valid", views.TitleValidViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("titles/", views.title_list, name="list"),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += router.urls
