from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState, TelegramMessage, TelegramUser, TelegramChat
from .bot import TelegramBot
from datetime import datetime
"""
from django.utils import timezone
import pytz
local_tz = pytz.timezone(settings.TIME_ZONE)
utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))
"""
import logging
lg = logging.getLogger('root')



"""
Next steps:
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

  #lg.debug('update type: '+ str(uptype))
  if not uptype == 'message':
    msg += 'update type is NOT a message; '
    lg.debug(msg)
    return

  chat = update.get_chat()
  chat_id = chat.get_id()
  #lg.debug('chat_id: '+ chat_id)
  message = update.get_message()
  message_id = message.message_id
  #lg.debug('message_id: '+ message_id)

  try:
    text = message.get_text()
    text_exists = True
    lg.debug('text: '+text[:50])
  except:
    text_exists = False
    lg.debug('no text')

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

  try:
    ts = message.date
    tgchat = TelegramChat.objects.get(telegram_id=chat_id)
    author = getattr(message, 'from', None)
    #lg.debug('username '+author.username)
    tguser, isnew = TelegramUser.objects.get_or_create(username=author.username)
    #lg.debug('tguser '+str(tguser))
  except:
    msg += 'in section user '
    lg.debug(msg)

  try:
    tgmessage, isnew = TelegramMessage.objects.get_or_create(
        message_id=message_id,
        author=tguser,
        group=tgchat,
        reply_to=None,
    )
  except:
    msg += 'Konnte nicht tgmessage objekt erstellen. - '
    lg.debug(msg)

  #lg.debug('start reply check')
  try:
    reply_to_message = getattr(message, 'reply_to_message', False)
    #lg.debug(reply_to_message)
    if reply_to_message:
      #lg.debug("msg IS A reply")
      rmid = reply_to_message.message_id
      reply_to_tgmessage = TelegramMessage.objects.get(message_id=rmid)
      #lg.debug(reply_to_tgmessage.text)
      tgmessage.reply_to = reply_to_tgmessage
    tgmessage.text = text

    dt = datetime.fromtimestamp(int(ts))
    #lg.debug(dt_utc)
    lg.debug(dt)
    tgmessage.date = dt
    tgmessage.save()
    msg = 'saved to DB: ' + text[:30] +'...'
    lg.debug(msg)
  except:
    msg += 'Konnte attribute des tgmessage objekts nicht speichern.'
    lg.debug(msg)
  return
