from django import  forms

from games.models import Game

class GameForm(forms.Form):
    class Meta:
        model = Game
        fields = ['name', 'release_date', 'platform', 'description', 'genres']