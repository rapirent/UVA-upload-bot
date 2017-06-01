# import telegram
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
# import logging

from telegram_bot.fsm import machine 
#from .fsm import TocMachine
from sendfile import sendfile
from io import BytesIO

import telegram

import logging
logger = logging.getLogger(__name__)



#bot = telegram.Bot(token=settings.HOOK_TOKEN)



def show_state(request):
    print("bot/state request")
    machine.graph.draw('my_stat_diagram.png', prog='dot', format='png')
    return sendfile(request, 'my_stat_diagram.png')


