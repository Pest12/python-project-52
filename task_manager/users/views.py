from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateUserForm
from .mixins import RulesMixin, DeleteProtectionMixin
from .models import Users


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
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')


class UpdateUser(RulesMixin,
                 SuccessMessageMixin,
                 UpdateView):
    model = Users
    form_class = CreateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('index_users')
    success_message = _('The user has been successfully changed')


class DeleteUser(RulesMixin,
                 DeleteProtectionMixin,
                 SuccessMessageMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index_users')
    protected_url = reverse_lazy('index_users')
    success_message = _('The user has been successfully deleted')
    protected_message = _("Cannot delete a user because it is in use")
