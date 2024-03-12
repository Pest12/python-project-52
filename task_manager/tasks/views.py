from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
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


class IsAuthorTask(UserPassesTestMixin):
    index_url = reverse_lazy('index_tasks')
    error_message = _('Only the author of the task can delete it.')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class IndexView(LoginRequiredMixin, FilterView):
    model = Tasks
    filterset_class = TasksFilter
    template_name = 'tasks/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task has been successfully changed')


class DeleteTask(LoginRequiredMixin, 
                 SuccessMessageMixin, 
                 IsAuthorTask, 
                 DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('index_tasks')
    success_message = _('The task was successfully deleted')


class ShowTask(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/show.html'
    context_object_name = 'task'
