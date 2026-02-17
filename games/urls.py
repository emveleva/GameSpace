from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<int:game_id>/', views.game_details, name='game_details'),
]
