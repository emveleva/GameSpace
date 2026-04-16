from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from games.models import Game


class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField(
        error_messages={
            'blank': 'Review text cannot be empty.',
        }
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Rating cannot be lower than 1.'),
            MaxValueValidator(5, message='Rating cannot be higher than 5.'),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.game.name} - Rating: {self.rating}"