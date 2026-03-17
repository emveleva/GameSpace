from django.urls import path

from . import views
from games import views as game_views

urlpatterns = [
    path('', views.platforms_list, name='platforms_list'),
    path('add_platform/', views.add_platform, name='add_platform'),
    path('<slug:slug>/edit/', views.edit_platform, name='edit_platform'),
    path('<slug:slug>/delete/', views.delete_platform, name='delete_platform'),
    path('<slug:slug>/platforms', game_views.games_by_platform, name='games_by_platform'),
]