from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm


class IndexView(View):
    """Root index view."""
    def get(self, request, *args, **kwargs):
        message = messages.get_messages(request)
        return render(request, 'index.html', context={
            'messages': message,
        })


class LoginUser(SuccessMessageMixin, LoginView):
    """User login page view."""
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUser(LogoutView):
    """User logout."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are logged out."))
        return super().dispatch(request, *args, **kwargs)
