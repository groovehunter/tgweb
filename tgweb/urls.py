"""tgweb URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from helfa_aux_dev_bot import urls as helfa_aux_dev_bot_urls

from . import views

#app_name = 'tgweb'

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='homebase'),
    path('page/<name>', views.page, name='page'),
    path('chat/', views.ChatListView.as_view(), name='chatindex'),#
    path('chat/<int:group_id>/', views.MessageListView.as_view()),#
    path('tguser/', views.TguserListView.as_view(), name='tguser-list-view'),
    path('tguser/<str:username>/', views.TguserDetailView.as_view(), name='tguser-detail-view'),
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
]

urlpatterns.append(path('helfa_dev_bot/', include(helfa_aux_dev_bot_urls)))
urlpatterns.append(path('helfa_aux_dev_bot/', include(helfa_aux_dev_bot_urls)))
