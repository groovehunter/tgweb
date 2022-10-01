
from djflow.PageController import PageController
from djflow.ViewController import DjMixin
from django.views.generic import ListView, DetailView
from django.conf import settings
if settings.ENV == 'dev':
  from helfa_aux_dev_bot.models import TelegramMessage, TelegramUser
if settings.ENV == 'prod':
  from helfa_dev_bot.models import TelegramMessage, TelegramUser

import logging
lg = logging.getLogger()


def page(request, name):
  ctrl = PageController(request)
  return ctrl.page(name)


def index(request):
  return page(request, 'one')

class TguserDetailView(DetailView):
  model = TelegramUser


class MessageListView(ListView, DjMixin):
    model = TelegramMessage
    template_name = 'item/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = DjMixin.get_context_data(self)
        context.update(c)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            #return self.access_denied()
            pass
        self.object_list = self.get_queryset()
        self.fields_noshow = []
        context = {}
        context['cat_defined'] = False
        #table = ItemTable(self.object_list) #, template_name="generic/table.html" )
        #context['table'] = table
        context.update(self.get_context_data())
        return self.render_to_response(context)
