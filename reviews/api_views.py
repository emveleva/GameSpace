from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewListAPI(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]