from django.urls import path
from reviews.api_views import ReviewListAPI

urlpatterns = [
    path('reviews/', ReviewListAPI.as_view()),
]