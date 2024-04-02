from django.forms import ModelForm
from .models import Statuses


class CreateStatusForm(ModelForm):
    """A form that creates a status."""
    class Meta:
        model = Statuses
        fields = ['name']
