from django.urls import path

from reviews.views import EditReviewView, DeleteReviewView

urlpatterns = [
    path('<int:pk>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('<int:pk>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]