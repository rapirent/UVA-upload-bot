from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

from emoji import emojize

from telegram_bot import uva

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


import logging
logger = logging.getLogger(__name__)

from .fsm import TocMachine
import pprint
pp = pprint.PrettyPrinter(indent=4)

machine = TocMachine(
    states=[
        'user',
        'UVA_UPLOAD',
        'FSM DIAGRAM',
        'ENROLL UVA'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'UVA_UPLOAD',
            'conditions': 'is_there_file_received'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'FSM DIAGRAM',
            'conditions': 'the /fsm was been called'
        },
        {
            'trigger': 'go_back',
            'source': [
                'UVA_UPLOAD',
                'FSM DIAGRAM'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    print(update)
    print(update.message)
    #update.message
    #'chat': {'last_name': 'ding', 'type': 'private', 'first_name': 'kuoteng', 'id': 339418741, 'username': 'rapirent'}
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def test(bot, update):
    update.message.reply_text('Hello World!')
    bot.sendPhoto(update.message.chat_id, photo='https://telegram.org/img/t_logo.png')
        #bot.sendPhote(update.message.chat_id, photo=open('/home/kuoteng/toc_project/kuoteng_bot/my_stat_diagram.png','rb'),caption='fuck'.encode('UTF-8'))

def nowDiagram(bot, update):
    machine.graph.draw('my_stat_diagram.png', prog='dot', format='png')
    bot.sendPhoto(update.message.chat_id, photo=open('my_stat_diagram.png','rb'))

def getFile(bot, update):
    file = bot.getFile(update.message.document.file_id)
    file_name = update.message.document.file_name
    number = int(file_name.strip(".cpp").strip('UVA-'))
    uva.submit(number,file.file_path)

def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("fsm", nowDiagram))
    dp.add_handler(CommandHandler("getFile", getFile))
    # on noncommand i.e message - echo the message on Telegram

    dp.add_handler(MessageHandler(Filters.document, getFile))
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

