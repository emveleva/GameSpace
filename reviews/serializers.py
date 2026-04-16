from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    game = serializers.CharField(source='game.name')

    class Meta:
        model = Review
        fields = [
            'id',
            'game',
            'user',
            'rating',
            'review',
            'created_at',
        ]