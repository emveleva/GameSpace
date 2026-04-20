from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from accounts.models import Profile
from common.mixins import DisableFieldsMixin


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        help_text='Required. Enter a valid email address.'
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        help_text='Required. 150 characters or fewer.'
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text='Enter password.'
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text='Re-enter your password.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class ProfileFormBasic(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        disabled=True,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['name', 'birthday', 'city', 'profile_picture']
        labels = {
            'name': 'Full Name',
            'birthday': 'Birthday',
            'city': 'City',
            'profile_picture': 'Profile Picture',
            'favorite_games': 'Favorite Games',
        }
        help_texts = {
            'name': 'Enter your full name',
            'birthday': 'Select your birth date',
            'city': 'Enter your city',
            'favorite_games': 'Select your favorite games',
        }
        error_messages = {
            'name': {
                'required': 'Full name is required.',
            },
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            "profile_picture": forms.FileInput(attrs={
                "id": "profile-picture-input",
                "class": "form-control"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self.instance, "user", None)
        if user:
            self.fields['username'].initial = user.username

class AddProfileForm(ProfileFormBasic):
    pass

class EditProfileForm(ProfileFormBasic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DeleteProfileForm(DisableFieldsMixin, ProfileFormBasic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)