from django.db import models
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    platform = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        avg = self.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else None