from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateStatusForm
from .models import Statuses
from task_manager.mixins import DeleteProtectionMixin, AuthRequiredMixin


class IndexView(AuthRequiredMixin, ListView):
    """Statuses page view."""
    model = Statuses
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class CreateStatus(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Status create page view."""
    form_class = CreateStatusForm
    template_name = 'create.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully created')
    extra_context = {
        'title': _("Create a status"),
        'button_text': _("Create")
    }


class UpdateStatus(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Status update page view."""
    model = Statuses
    form_class = CreateStatusForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully changed')
    extra_context = {
        'title': _("Status change"),
        'button_text': _("Change")
    }


class DeleteStatus(AuthRequiredMixin,
                   SuccessMessageMixin,
                   DeleteProtectionMixin,
                   DeleteView):
    """Status delete page view."""
    model = Statuses
    template_name = 'delete.html'
    success_url = reverse_lazy('index_statuses')
    success_message = _('The status has been successfully deleted')
    protected_message = _('It is not possible to delete the '
                          'status because it is in use')
    protected_url = reverse_lazy('index_statuses')
    extra_context = {
        'title': _("Deleting a status"),
        'button_text': _("Yes, delete")
    }
