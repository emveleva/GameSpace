from rest_framework import serializers
from games.models import Game


class GameSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    platforms = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id',
            'name',
            'release_date',
            'platforms',
            'genres',
            'description',
            'image_url',
            'created_by',
            'average_rating',
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()