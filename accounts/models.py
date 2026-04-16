from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db import models
from games.models import Game


def validate_birthday(value):
    if value > now().date():
        raise ValidationError('Birthday cannot be in the future.')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    name = models.CharField(
        max_length=100,
        blank=True,
        validators=[MinLengthValidator(2, message='Name must be at least 2 characters long.')],
        error_messages={'max_length': 'Name cannot exceed 100 characters.'}
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        validators=[MinLengthValidator(2, message='City must be at least 2 characters long.')],
        error_messages={'max_length': 'City cannot exceed 100 characters.'}
    )

    birthday = models.DateField(
        blank=True,
        null=True,
        validators=[validate_birthday]
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png'],
            message='Only JPG and PNG files are allowed.'
        )]
    )

    favorite_games = models.ManyToManyField(Game, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def reviews(self):
        return self.user.reviews.all()