from django import forms

from common.mixins import DisableFieldsMixin
from genres.models import Genre


class GenreFormBasic(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name':'Genre Name',
        }
        help_texts = {
            'name':'Genre Name',
        }
        error_messages = {
            'name': {
                'required': 'Genre name is required',
                'unique': 'This genre name already exists.',
                'blank': 'Please provide a title.',
            }
        }

class AddGenreForm(GenreFormBasic):
    ...

class EditGenreForm(GenreFormBasic):
    ...

class DeleteGenreForm(DisableFieldsMixin, GenreFormBasic):
    ...