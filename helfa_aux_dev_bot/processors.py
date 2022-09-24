from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState, TelegramMessage, TelegramUser, TelegramChat
from .bot import TelegramBot

import logging
lg = logging.getLogger('root')
from datetime import datetime

"""
@processor(state_manager, from_states=state_types.All)
def hello_world(bot: TelegramBot, update: Update, state: TelegramState):
    bot.sendMessage(update.get_chat().get_id(), 'Hello!')
"""

@processor(state_manager, from_states=state_types.All)
def save_message(bot: TelegramBot, update: Update, state: TelegramState):
  msg = 'Es ist ein Fehler aufgetreten beim Speichern.'
  uptype = update.type()
  chat = update.get_chat()
  chat_id = chat.get_id()
  if not uptype == 'message':
    lg.debug('update type: ', uptype)
    bot.sendMessage(chat_id, msg)
    return

  try:
    message = update.get_message()
    text = message.get_text()
    ts = message.date
    message_id = message.message_id
    lg.debug('milestone', message_id)
    lg.debug('chat_id', chat_id, ts)
    tgchat = TelegramChat.objects.get(telegram_id=chat_id)
    author = getattr(message, 'from')
    #username = 'groovehunter'
    tguser, isnew = TelegramUser.objects.get_or_create(username=author.username)
    tgmessage, isnew = TelegramMessage.objects.get_or_create(
        message_id=message_id,
        author=tguser,
        group=tgchat,
    )
    tgmessage.text = text
    d = datetime.fromtimestamp(int(ts))
    tgmessage.date = d
    tgmessage.save()
    msg = 'saved to DB: ' + text[:30] +'...'
    bot.sendMessage(chat_id, msg)
  except:
    pass
    bot.sendMessage(chat_id, msg)
