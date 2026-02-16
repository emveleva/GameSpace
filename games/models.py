from django.db import models

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

    def __str__(self):
        return self.name