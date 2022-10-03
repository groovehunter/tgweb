from django.db import models
from django.db.models import CASCADE
from django.urls import reverse

from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState
#from django_tgbot.types.message import Message

class TelegramUser(AbstractTelegramUser):
  colors = {
    3:  'red',
    4:  'orange',
    5:  'lightblue',
    6:  'grey',
    7:  'lightgrey',
    8:  'white',
    9:  'green',
    10: 'blue',
    11: 'gold',
    12: 'lightgreen',
  }
  def get_absolute_url(self):
    return reverse('tguser-detail-view', args=[str(self.username)])

  def get_color(self):
    return self.colors[len(self.username)]

  color = property(get_color)


class TelegramChat(AbstractTelegramChat):

  def __str__(self):
    return self.title


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')

class TelegramMessage(models.Model):
  message_id  = models.IntegerField()
  date        = models.DateTimeField(null=True)
  author = models.ForeignKey(
    TelegramUser,
    on_delete = models.CASCADE,
    blank = False,
    default = None,
  )
  group = models.ForeignKey(
    TelegramChat,
    on_delete = models.CASCADE,
    blank = True,
    default = None,
  )
  text = models.TextField()
  reply_to = models.ForeignKey(
    'self',
    on_delete = models.CASCADE,
    blank = True,
    default = None,
    null = True,
  )

  def __str__(self):
    return self.text[:150]
"""
"""
