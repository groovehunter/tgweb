
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.shortcuts import render, redirect
from djflow.ViewController import DjMixin

import logging
lg = logging.getLogger('root')

class UserListView(LoginRequiredMixin, ListView, DjMixin):
    model = get_user_model()
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

class UserDetailView(LoginRequiredMixin, DetailView, DjMixin):
    model = get_user_model()
    template_name = 'users/profile.html'
    pk_url_kwargs = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

### login & logout functions

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        lg.info('user logged in')
        return redirect('/')
    else:
        c = {}
        return render(request, 'access_denied.html', c)

def logout_user(request):
    logout(request)
    return redirect('/')
