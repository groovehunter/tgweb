
from djflow.PageController import PageController
from djflow.ViewController import DjMixin
from django.generic.views import ListView

import logging
lg = logging.getLogger()


def page(request, name):
  ctrl = PageController(request)
  return ctrl.page(name)


def index(request):
  return page(request, 'one')

class MessageListView(ListView, DjMixin):
    model = TelegramMessage
    template_name = 'item_list.html'

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
