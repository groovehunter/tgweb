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

"""
Next steps:
check for reply_to attribute
photos flat in table und message-id dazu?
oder multi photo DB modell?

unterscheiden in anwendungsfall; 
ob tgweb oder ob verschenka 
"""

@processor(state_manager, from_states=state_types.All)
def save_message(bot: TelegramBot, update: Update, state: TelegramState):
  lg.debug("............................................")
  lg.debug("save message processor started...")
  msg = 'Ein Fehler ist aufgetreten: '
  text_exists = False
  reply_to = False

  uptype = update.type()
  lg.debug('update type: '+ uptype)
  chat = update.get_chat()
  chat_id = chat.get_id()
  lg.debug('chat_id: '+ chat_id)
  if not uptype == 'message':
    bot.sendMessage(chat_id, msg)
    return
  message = update.get_message()
  message_id = message.message_id
  lg.debug('message_id: '+ message_id)

  try:
    text = message.get_text()
    text_exists = True
    lg.debug('text: '+text)
  except:
    text_exists = False
    lg.debug('no text')
  try:
    reply_to = message.reply_to_message
    lg.debug(reply_to)
  except:
    lg.debug("msg was no reply")

  if not text_exists:
    lg.debug('IF no text')
    try:
      photo = message.photo
      caption = photo.caption
    except:
      msg += 'get photo failed.'
      lg.debug(msg)
    try:
      doc = message.document
      lg.debug('got doc okay')
    except:
      msg += 'get doc failed.'
      lg.debug(msg)
      #bot.sendMessage(chat_id, msg)
      #return


  try:
    ts = message.date
    tgchat = TelegramChat.objects.get(telegram_id=chat_id)
    author = getattr(message, 'from')
    #username = 'groovehunter'
    tguser, isnew = TelegramUser.objects.get_or_create(username=author.username)

    if reply_to:
      tgmsg = reply_to.message_id
    else:
      tgmsg = None
    lg.debug("set reply_to to "+str(tgmsg))
  except:
    msg += 'in section user / reply_to; '
    lg.debug(msg)

  try:
    tgmessage, isnew = TelegramMessage.objects.get_or_create(
        message_id=message_id,
        author=tguser,
        group=tgchat,
        reply_to=tgmsg,
    )
  except:
    msg += 'Konnte nicht tgmessage objekt erstellen.'
    lg.debug(msg)
    #bot.sendMessage(chat_id, msg)
    #return

  try:
    tgmessage.text = text
    d = datetime.fromtimestamp(int(ts))
    tgmessage.date = d
    tgmessage.save()
    msg = 'saved to DB: ' + text[:30] +'...'
    lg.debug(msg)
    #bot.sendMessage(chat_id, msg)
  except:
    msg += 'Konnte attribute des tgmessage objekts nicht speichern.'
    lg.debug(msg)
    #bot.sendMessage(chat_id, msg)
    return

