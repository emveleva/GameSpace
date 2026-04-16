from django.urls import path
from games.api_views import GameListAPI, GameDetailAPI

urlpatterns = [
    path('games/', GameListAPI.as_view()),
    path('games/<int:id>/', GameDetailAPI.as_view()),
]