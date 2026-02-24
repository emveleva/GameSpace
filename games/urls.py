from django.urls import path

from reviews.views import AddReviewView
from . import views

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<int:game_id>/', views.game_details, name='game_details'),
    path('add_game/', views.add_game, name='add_game'),
    path('<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('<int:game_id>/delete/', views.delete_game, name='delete_game'),
    path('<int:game_id>/review/', AddReviewView.as_view(), name='add_review')
]
