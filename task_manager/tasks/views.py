from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Tasks
from .forms import CreateTasksForm
from django.views.generic.detail import DetailView
from .filters import TasksFilter
from django_filters.views import FilterView
from task_manager.mixins import OnlyAuthorDeletionMixin, AuthRequiredMixin


class IndexView(AuthRequiredMixin, FilterView):
    """Tasks page view."""
    model = Tasks
    filterset_class = TasksFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class CreateTask(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Task create page view."""
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'create.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task has been successfully created')
    extra_context = {
        'title': _("Create a task"),
        'button_text': _("Create")
    }

    def form_valid(self, form):
        """Set current user as the task's author."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Task update page view."""
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task has been successfully changed')
    extra_context = {
        'title': _("Changing the task"),
        'button_text': _("Change")
    }


class DeleteTask(AuthRequiredMixin,
                 OnlyAuthorDeletionMixin,
                 SuccessMessageMixin,
                 DeleteView):
    """Task delete page view."""
    model = Tasks
    template_name = 'delete.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task was successfully deleted')
    permission_denied_message = _('Only the author of the task can delete it.')
    permission_denied_url = reverse_lazy('index_tasks')
    extra_context = {
        'title': _("Deleting a task"),
        'button_text': _("Yes, delete")
    }


class ShowTask(AuthRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/show.html'
    context_object_name = 'task'
