from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateUserForm
from .models import Users
from task_manager.mixins import AuthRequiredMixin, UserPermissionMixin, \
    DeleteProtectionMixin


class IndexView(ListView):
    model = Users
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context


class CreateUser(SuccessMessageMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')
    extra_context = {
        'title': _("Sign up"),
        'button_text': _("Register")
    }


class UpdateUser(AuthRequiredMixin,
                 UserPermissionMixin,
                 SuccessMessageMixin,
                 UpdateView):
    model = Users
    form_class = CreateUserForm
    template_name = 'update.html'
    success_url = reverse_lazy('index_users')
    success_message = _('The user has been successfully changed')
    permission_url = reverse_lazy('index_users')
    permission_message = _('You do not have the rights to change another user.')
    extra_context = {
        'title': _("Changing the user"),
        'button_text': _("Change")
    }


class DeleteUser(AuthRequiredMixin,
                 UserPermissionMixin,
                 DeleteProtectionMixin,
                 SuccessMessageMixin,
                 DeleteView):
    model = Users
    template_name = 'delete.html'
    success_url = reverse_lazy('index_users')
    success_message = _('The user has been successfully deleted')
    permission_url = reverse_lazy('index_users')
    permission_message = _('You do not have the rights to change another user.')
    protected_url = reverse_lazy('index_users')
    protected_message = _("Cannot delete a user because it is in use")
    extra_context = {
        'title': _("Deleting a user"),
        'button_text': _("Yes, delete")
    }
