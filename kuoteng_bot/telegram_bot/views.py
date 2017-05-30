# import telegram
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
# import logging

from .telegrambot import machine 
#from .fsm import TocMachine
from sendfile import sendfile
from io import BytesIO

import telegram

import logging
logger = logging.getLogger(__name__)



#bot = telegram.Bot(token=settings.HOOK_TOKEN)



def showState(request):
    machine.graph.draw('my_stat_diagram.png', prog='dot', format='png')
    return sendfile(request, 'my_stat_diagram.png')

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def webhook(request):
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)

    print('')
    dp = Updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    return 'ok'


def _set_webhook():
    print('fuck')
    updater = Updater(token=settings.HOOK_TOKEN)
#    updater.start_webhook(listen=settings.HOOK_URL, port=8000, url_path='hook')
    status = updater.bot.set_webhook(settings.HOOK_URL + '/bot/hook')
    if not status:
        print('webhook setup failed')
    else:
        print('Your webhook URL has been set to "{}"'.format(settings.HOOK_URL))

