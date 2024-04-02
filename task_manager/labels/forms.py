from django.forms import ModelForm
from .models import Labels


class CreateLabelsForm(ModelForm):
    """A form that creates a label."""
    class Meta:
        model = Labels
        fields = ['name']
