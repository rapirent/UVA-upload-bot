from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot

from emoji import emojize

from telegram_bot import uva

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


import logging
logger = logging.getLogger(__name__)

from .fsm import TocMachine

machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2'
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
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def test(bot, update):
    update.message.reply_text('Hello World!')
    print('test')
    try:
        print('fuck')
        bot.sendPhoto(update.message.chat_id, photo='https://telegram.org/img/t_logo.png')
        #bot.sendPhote(update.message.chat_id, photo=open('/home/kuoteng/toc_project/kuoteng_bot/my_stat_diagram.png','rb'),caption='fuck'.encode('UTF-8'))
    except error:
        print('??')
        print(error)
def nowDiagram(bot, update):
    pass

def getFile(bot, update):
    file = bot.getFile(update.message.document.file_id)
    file_name = update.message.document.file_name


    submit(file_name.strip('c','p'),file.file_path)

def main():
    logger.info("Loading handlers for telegram bot")

    dp = DjangoTelegramBot.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("getFile", getFile))
    # on noncommand i.e message - echo the message on Telegram

    dp.add_handler(MessageHandler(Filters.document, getFile))
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

