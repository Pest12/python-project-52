from django.forms import ModelForm
from .models import Tasks


class CreateTasksForm(ModelForm):
    """A form that creates a task."""
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']
