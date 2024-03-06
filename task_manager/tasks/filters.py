import django_filters
from task_manager.users.models import Users
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from django import forms
from django.utils.translation import gettext as _


class TasksFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=('Status'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Users.objects.all(),
        label=('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=('Label'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    user_tasks = django_filters.BooleanFilter(
        field_name='author',
        label='',
        help_text=_('Only your own tasks'),
        method='filter_user_tasks',
        widget=forms.CheckboxInput(),
    )

    def filter_user_tasks(self, queryset, name, value):
        if value:
            user_id = self.request.user.id
            return queryset.filter(author_id=user_id)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'user_tasks']
