from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import Tasks
from .forms import CreateTasksForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .filters import TasksFilter
from django_filters.views import FilterView
from task_manager.mixins import AuthorDeletionMixin


class IndexView(LoginRequiredMixin, FilterView):
    model = Tasks
    filterset_class = TasksFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task has been successfully changed')
    extra_context = {
        'title': _("Changing the task"),
        'button_text': _("Change")
    }


class DeleteTask(LoginRequiredMixin,
                 AuthorDeletionMixin,
                 SuccessMessageMixin,
                 DeleteView):
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


class ShowTask(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/show.html'
    context_object_name = 'task'
