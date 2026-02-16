from django import  forms

from reviews.models import Review

class GameForm(forms.Form):
    class Meta:
        model = Review
        fields = ['game', 'review', 'rating', 'author']