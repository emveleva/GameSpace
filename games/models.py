from django.db import models
from django.db.models import Avg


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
        error_messages={
            'blank': 'Game name is required',
            'max_length': 'Game name must be less than 100 characters',
        }
    )
    release_date = models.DateField()
    platforms = models.ManyToManyField(Platform)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else None