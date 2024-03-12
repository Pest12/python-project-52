from django.shortcuts import redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateLabelsForm
from .models import Labels
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateLabelsForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label was created successfully')


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = CreateLabelsForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label has been successfully changed')


class DeleteLabel(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label was successfully deleted')
    error_del_message = _('It is not possible to delete a label because it is being used')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR,
                self.error_del_message
            )
            return redirect(reverse_lazy('index_labels'))
