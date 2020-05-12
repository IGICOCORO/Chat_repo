from django.urls import path, include
from rest_framework import routers
from .api import *
from . import views

router = routers.DefaultRouter()
router.register("contact", ContactViewset)
router.register("message", MessageViewset)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.Home.as_view(), name='home'),
    path("<int:id_user>", views.Chat.as_view(), name='chat'),
]

