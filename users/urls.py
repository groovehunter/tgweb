from django.urls import path
from .views import login_user, logout_user
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login_user', login_user,      name='login'),
    path('logout', logout_user,    name='logout'),
    path('profile/<str:username>/', views.UserDetailView.as_view(), name='profile'),
#    path('profile/', views.UserDetailView.as_view(), name='profile'),
    path('index', login_required(views.UserListView.as_view()), name='user-list-view'),
    path('login', auth_views.LoginView.as_view())
]
