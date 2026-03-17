from django.urls import path

from . import views
from games import views as game_views

urlpatterns = [
    path('', views.genres_list, name='genres_list'),
    path('add_genre/', views.add_genre, name='add_genre'),
    path('<slug:slug>/edit/', views.edit_genre, name='edit_genre'),
    path('<slug:slug>/delete/', views.delete_genre, name='delete_genre'),
    path('<slug:slug>/games', game_views.games_by_genre, name='games_by_genre'),
]