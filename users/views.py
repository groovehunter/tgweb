
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.views.generic import CreateView, ListView, DetailView, TemplateView
#from users.models import CustomUser
from django.conf import settings
from django.shortcuts import render
from djflow.ViewController import DjMixin

import logging
lg = logging.getLogger('root')

class UserListView(ListView, DjMixin):
    model = get_user_model()
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            #return self.access_denied()
            pass
        context = self.get_context_data()
        return self.render_to_response(context)


class UserDetailView(DetailView, DjMixin):
    model = get_user_model()
    template_name = 'users/profile.html'
    pk_url_kwargs = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs)

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    return redirect('page/one')

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('users/login.html')
    else:
        form = AuthenticationForm()
    return render(request,'user/login.html', {'form':form})
