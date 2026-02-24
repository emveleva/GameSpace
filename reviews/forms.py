from django import  forms

from common.mixins import DisableFieldsMixin
from reviews.models import Review

class ReviewFormBasic(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'rating', 'review']

        labels = {
            'author': 'Author',
            'rating': 'Rating (1-5)',
            'review': 'Review',
        }

        help_texts = {
            'rating': 'Rate the game from 1 (worst) to 5 (best).',
            'review': 'Write at least 10 characters.',
        }

        error_messages = {
            'rating': {
                'min_value': 'Rating cannot be lower than 1.',
                'max_value': 'Rating cannot be higher than 5.',
            },
            'review': {
                'blank': 'Review text is required.',
            }
        }

        widgets = {
            'review': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your honest opinion...',
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
            }),
        }

class AddReviewForm(ReviewFormBasic):
    ...

class EditReviewForm(ReviewFormBasic):
    ...

class DeleteReviewForm(DisableFieldsMixin, ReviewFormBasic):
    ...