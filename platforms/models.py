from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Platform(models.Model):
    name = models.CharField(
        max_length=50,
        unique = True,
        validators = [MinLengthValidator(3)],
        help_text = 'Enter a unique platform name (at least 3 characters).',
        error_messages = {
            'blank': 'Platform name is required',
            'unique': 'A platform with this name already exists.',
            'max_length': 'Platform name must be less than 50 characters',
        }
    )
    slug = models.SlugField(unique=True)
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text='Optional: Provide an image URL for the platform.'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("games_by_platform", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
