from django.urls import path, include
from rest_framework import routers
from .api import *
from . import views

router = routers.DefaultRouter()
router.register("contact", ContactSerializer, basename='contact')
router.register("message", MessageSerializer, basename='contact')

urlpatterns = [
    # path("api/", include(router.urls)),
    path("", views.Home.as_view(), name='home'),
    path("<id_user>", views.Chat.as_view(), name='chat'),
]

