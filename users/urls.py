from django.urls import path
from .views import login_user, logout_user
from . import views

app_name = 'users'

urlpatterns = [
    path('login', login_user,      name='login'),
    path('logout', logout_user,    name='out'),
    path('profile/<str:username>', views.UserDetailView.as_view(), name='profile'),
    path('profile/', views.UserDetailView.as_view(), name='profile'),
    path('index', views.UserListView.as_view(), name='user-list-view'),
#    path('login', LoginView.as_view())
]
