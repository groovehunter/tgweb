"""tgweb URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from .views import index, page
from helfa_aux_dev_bot import urls as helfa_aux_dev_bot_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='home'),
    path('page/<name>', page, name='page'),
    path('helfa_aux_dev_bot/', include(helfa_aux_dev_bot_urls)),
    ### apps
#    path('users/', include('users.urls')),

]
