from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text='Enter a unique game name (at least 3 characters).',
        error_messages = {
            'blank': 'Game name is required',
            'unique': 'A game with this name already exists.',
            'max_length': 'Game name must be less than 100 characters',
        }
    )
    release_date = models.DateField(
        help_text='Select the official release date.'
    )
    platforms = models.ManyToManyField(Platform)
    description = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text='Write a detailed description (at least 10 characters).',
        error_messages={
            'blank': 'Description is required.',
        }
    )
    genres = models.ManyToManyField(Genre)
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text='Optional: Provide an image URL for the game.'
    )

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else None

    def get_absolute_url(self):
        return reverse("game_details", kwargs={"game_id": self.pk})