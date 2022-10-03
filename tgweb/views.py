
from djflow.PageController import PageController
from djflow.ViewController import DjMixin
from django.views.generic import ListView, DetailView
from django.conf import settings
if settings.ENV == 'dev':
  from helfa_aux_dev_bot.models import TelegramMessage, TelegramUser, TelegramChat
if settings.ENV == 'prod':
  from helfa_dev_bot.models import TelegramMessage, TelegramUser, TelegramChat

import logging
lg = logging.getLogger()


def page(request, name):
  ctrl = PageController(request)
  return ctrl.page(name)


def index(request):
  return page(request, 'one')

class TguserDetailView(DetailView, DjMixin):
  model = TelegramUser
  #pk_slug_kwarg = 'username'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    c = DjMixin.get_context_data(self)
    context.update(c)
    return context
  def get_object(self, queryset=None):
    return TelegramUser.objects.get(username=self.kwargs.get("username"))

class TguserListView(ListView, DjMixin):
  model = TelegramUser
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    c = DjMixin.get_context_data(self)
    context.update(c)
    return context


class ChatListView(ListView, DjMixin):
  model = TelegramChat
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      c = DjMixin.get_context_data(self)
      context.update(c)
      return context


class MessageListView(ListView, DjMixin):
  model = TelegramMessage
  template_name = 'item/item_list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    c = DjMixin.get_context_data(self)
    context.update(c)
    return context

  def get_queryset(self):
    return TelegramMessage.objects.filter(group__id=self.kwargs['group_id']).order_by('date').reverse()

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
