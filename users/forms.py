from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = ['username',
                  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use")
        return email


class CustomUserLoginForm(AuthenticationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def __int__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     super(CustomUserLoginForm, self).__init__(*args, **kwargs)

