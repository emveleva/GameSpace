from django import forms

from common.mixins import DisableFieldsMixin
from genres.models import Genre
from platforms.models import Platform


class PlatformFormBasic(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name']
        labels = {
            'name':'Platform Name',
        }
        help_texts = {
            'name':'Platform Name',
        }
        error_messages = {
            'name': {
                'required': 'Platform name is required',
                'unique': 'This Platform name already exists.',
                'blank': 'Please provide a title.',
            }
        }

class AddPlatformForm(PlatformFormBasic):
    ...

class EditPlatformForm(PlatformFormBasic):
    ...

class DeletePlatformForm(DisableFieldsMixin, PlatformFormBasic):
    ...