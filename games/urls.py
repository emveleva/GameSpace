from django.urls import path

from reviews.views import AddReviewView
from . import views
from .views import DeleteGameView, EditGameView, AddGameView, GameDetailsView, GamesListView

urlpatterns = [
    path('', GamesListView.as_view(), name='games_list'),
    path('<int:game_id>/', GameDetailsView.as_view(), name='game_details'),
    path('add_game/', AddGameView.as_view(), name='add_game'),
    path('<int:game_id>/edit/', EditGameView.as_view(), name='edit_game'),
    path('<int:game_id>/delete/', DeleteGameView.as_view(), name='delete_game'),
    path('<int:game_id>/review/', AddReviewView.as_view(), name='add_review')
]
