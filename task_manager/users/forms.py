from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _


class CreateUserForm(UserCreationForm):
    """A form that creates a user."""
    first_name = forms.CharField(
        required=True, max_length=150, label=_('First name')
    )
    last_name = forms.CharField(
        required=True, max_length=150, label=_('Last name')
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username',
                  'password1', 'password2']
