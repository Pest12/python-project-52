from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateLabelsForm
from .models import Labels
from task_manager.mixins import DeleteProtectionMixin, AuthRequiredMixin


class IndexView(AuthRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateLabel(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateLabelsForm
    template_name = 'create.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label was created successfully')
    extra_context = {
        'title': _("Create a label"),
        'button_text': _("Create")
    }


class UpdateLabel(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = CreateLabelsForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label has been successfully changed')
    extra_context = {
        'title': _("Changing the label"),
        'button_text': _("Change")
    }


class DeleteLabel(AuthRequiredMixin,
                  SuccessMessageMixin,
                  DeleteProtectionMixin,
                  DeleteView):
    model = Labels
    template_name = 'delete.html'
    success_url = reverse_lazy('index_labels')
    success_message = _('The label was successfully deleted')
    protected_message = _('It is not possible to delete a '
                          'label because it is being used')
    protected_url = reverse_lazy('index_labels')
    extra_context = {
        'title': _("Deleting a label"),
        'button_text': _("Yes, delete")
    }
