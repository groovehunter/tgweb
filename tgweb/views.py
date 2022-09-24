
from djflow.PageController import PageController
#from django.views.decorators.csrf import ensure_csrf_cookie

import logging
lg = logging.getLogger()


#@ensure_csrf_cookie


def page(request, name):
  ctrl = PageController(request)
  return ctrl.page(name)


def index(request):
  return page(request, 'one')



