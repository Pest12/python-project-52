from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import LoginUserForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        message = messages.get_messages(request)
        return render(request, 'index.html', context={
            'messages': message,
        })
    

class LoginUser(SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    success_message = _('You are logged in')


class LogoutUser(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _("You are logged out."))
        return super().dispatch(request, *args, **kwargs)