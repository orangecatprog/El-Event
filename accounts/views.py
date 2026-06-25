from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import AccountForm, RegisterForm


class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard-home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard-home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return super().form_valid(form)


class AccountView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountForm
    template_name = 'accounts/account.html'
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return self.request.user
