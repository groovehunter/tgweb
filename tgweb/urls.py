"""tgweb URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
if settings.ENV == 'dev':
  from helfa_aux_dev_bot import urls as helfa_aux_dev_bot_urls
if settings.ENV == 'prod':
  from helfa_dev_bot import urls as helfa_dev_bot_urls

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='homebase'),
    path('page/<name>', views.page, name='page'),
    path('chat/<int:chat_id>/', views.MessageListView.as_view()),#
    path('tguser/<int:tguser_id>/', views.TguserDetailView.as_view(), name='tguser-detail-view'),
    #path('helfa_aux_dev_bot/', include(helfa_aux_dev_bot_urls)),
    path("admin/", admin.site.urls),
    ### apps
#    path('users/', include('users.urls')),

]
if settings.ENV == 'dev':
  urlpatterns.append(path('helfa_aux_dev_bot/', include(helfa_aux_dev_bot_urls)))

if settings.ENV == 'prod':
  urlpatterns.append(path('helfa_dev_bot/', include(helfa_dev_bot_urls)))

