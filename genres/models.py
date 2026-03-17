from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text='Enter a unique genre name (at least 3 characters).',
        error_messages={
            'blank': 'Genre name is required',
            'unique': 'A genre with this name already exists.',
            'max_length': 'Genre name must be less than 50 characters',
        }
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("games_by_genre", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)