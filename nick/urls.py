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
    path("movies/", views.get_movies, name="get_movies"),
    path("movies/<int:id>", views.get_title, name="get_single_movie"),
    path("genres/<str:genre>", views.get_movies, name="get_movies_by_genre"),
    path("search/", views.search, name="search")
]

urlpatterns += router.urls
