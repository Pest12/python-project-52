from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.db.models import ProtectedError


class RulesMixin(AccessMixin):
    def has_permission(self):
        return self.get_object().pk == self.request.user.pk

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.ERROR,
                _('You are not logged in! Please log in.')
            )
            return redirect('login')
        elif not self.has_permission():
            messages.add_message(
                request, messages.ERROR,
                _('You do not have the rights to change another user.')
            )
            return redirect('index_users')
        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(
                request, messages.ERROR,
                self.protected_message)
            return redirect(self.protected_url)
