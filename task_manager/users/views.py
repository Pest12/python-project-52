from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import CreateUserForm
from task_manager.mixins import NoAuthorizationMixin, NoPermissionMixin


MESS_PERMISSION = _("You do not have permission to modify another user.")

class IndexView(ListView): 
    model = get_user_model()
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
    success_message = _('You have successfully registred')


class UpdateUser(NoAuthorizationMixin, NoPermissionMixin, 
                 SuccessMessageMixin, UpdateView):
    form_class = CreateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('index_users')
    success_message = _('User successfully changed')

    def get(self, request, *args, **kwargs):
        user_id = self.get_object().id
        url_id = kwargs.get('id')
        if url_id != user_id:
            messages.add_message(self.request, messages.ERROR,
                                 MESS_PERMISSION)
            return redirect(reverse_lazy('index_users'))

        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

    def form_valid(self, form):
        password = form.cleaned_data.get('password1')
        if password:
            self.object.set_password(password)
        return super().form_valid(form)


class DeleteUser(NoAuthorizationMixin, NoPermissionMixin, 
                 SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    success_url = reverse_lazy('index_users')
    success_message = _('User deleted sucessfully')

    def get(self, request, *args, **kwargs):
        user_id = self.get_object().id
        url_id = kwargs.get('id')
        if url_id != user_id:
            messages.add_message(self.request, messages.ERROR,
                                 MESS_PERMISSION)
            return redirect(reverse_lazy('index_users'))

        return super().get(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

    def post(self,request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR,
                _("The user cannot be deleted because it is in use.")
            )
            return redirect(reverse_lazy('index_users'))