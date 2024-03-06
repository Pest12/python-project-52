from django.forms import ModelForm
from .models import Statuses


class CreateStatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ['name']
