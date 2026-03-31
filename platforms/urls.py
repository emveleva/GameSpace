from django.urls import path

from games.views import GamesByPlatformView
from . import views
from games import views as game_views
from .views import PlatformsListView, AddPlatformView, EditPlatformView, DeletePlatformView

urlpatterns = [
    path('', PlatformsListView.as_view(), name='platforms_list'),
    path('add_platform/', AddPlatformView.as_view(), name='add_platform'),
    path('<slug:slug>/edit/', EditPlatformView.as_view(), name='edit_platform'),
    path('<slug:slug>/delete/', DeletePlatformView.as_view(), name='delete_platform'),
    path('<slug:slug>/platforms', GamesByPlatformView.as_view(), name='games_by_platform'),
]