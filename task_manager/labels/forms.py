from django.forms import ModelForm
from .models import Labels


class CreateLabelsForm(ModelForm):
    class Meta:
        model = Labels
        fields = ['name']
