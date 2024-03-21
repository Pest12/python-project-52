from django.shortcuts import redirect
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateStatusForm
from .models import Statuses
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateStatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully created')
    extra_context = {
        'title': _("Create a status"),
        'button_text': _("Create")
    }


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = CreateStatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully changed')
    extra_context = {
        'title': _("Status change"),
        'button_text': _("Change")
    }


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Statuses
    template_name = 'delete.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully deleted')
    error_del_message = _('It is not possible to delete the '
                          'status because it is in use')
    extra_context = {
        'title': _("Deleting a status"),
        'button_text': _("Yes, delete")
    }

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR,
                self.error_del_message
            )
            return redirect(reverse_lazy('index_statuses'))
