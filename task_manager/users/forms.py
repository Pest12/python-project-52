from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from string import ascii_lowercase, ascii_uppercase, digits
from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')
        
        