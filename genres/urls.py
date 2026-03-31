from django.urls import path

from games.views import GamesByGenreView
from . import views
from games import views as game_views
from .views import GenresListView, AddGenreView, EditGenreView, DeleteGenreView

urlpatterns = [
    path('', GenresListView.as_view(), name='genres_list'),
    path('add_genre/', AddGenreView.as_view(), name='add_genre'),
    path('<slug:slug>/edit/', EditGenreView.as_view(), name='edit_genre'),
    path('<slug:slug>/delete/', DeleteGenreView.as_view(), name='delete_genre'),
    path('<slug:slug>/games', GamesByGenreView.as_view(), name='games_by_genre'),
]