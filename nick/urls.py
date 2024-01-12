from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'titles', views.TitleViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls