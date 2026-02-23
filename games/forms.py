from django import  forms

from games.models import Game

class GameFormBasic(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Write a short description about the game...',
                'rows': 5,
            }),
            'release_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'genres': forms.CheckboxSelectMultiple(),
            'platforms': forms.CheckboxSelectMultiple(),
        }

class AddGameForm(GameFormBasic):
    pass

class EditGameForm(GameFormBasic):
    pass

class DeleteGameForm(GameFormBasic):
    pass