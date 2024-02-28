from django.forms import ModelForm
from .models import Tasks


class CreateTasksForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']