from django import  forms

from common.mixins import DisableFieldsMixin
from games.models import Game

class GameFormBasic(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        labels = {
            'name':'Game Title',
            'description':'Game Description',
            'release_date':'Release Date',
        }
        help_texts = {
            'name':'Game Name',
            'description':'Write something interesting about the game.',
        }
        error_messages = {
            'name': {
                'required': 'Game name is required',
                'unique': 'This game title already exists.',
                'blank': 'Please provide a title.',
            }
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Write a short description about the game...',
                'rows': 5,
            }),
            'release_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'multi-select',
            }),
            'platforms': forms.SelectMultiple(attrs={
                'class': 'multi-select',
            }),
        }

class AddGameForm(GameFormBasic):
    ...

class EditGameForm(GameFormBasic):
    ...

class DeleteGameForm(DisableFieldsMixin, GameFormBasic):
    ...

class GameSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search games...',
        }),
        error_messages={
            'max_length': 'Search query too long.',
        }
    )