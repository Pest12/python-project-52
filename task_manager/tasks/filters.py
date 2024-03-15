import django_filters
from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users
from task_manager.labels.models import Labels
from django import forms
from django.utils.translation import gettext as _


class TasksFilter(django_filters.FilterSet):
    def filter_user_tasks(self, queryset, author, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=Users.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    labels = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Labels.objects.all(),
        label=_('Labels'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    self_tasks = django_filters.BooleanFilter(
        label=_("Only your own tasks"),
        method="filter_user_tasks",
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'self_tasks']
