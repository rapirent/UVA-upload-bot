#_*_ encoding: utf-8 _*_
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from emoji import emojize
from telegram_bot import uva
import requests.packages.urllib3


#database
from telegram_bot.models import User


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
    try:
        search_id = User.objects.get(telegram_id=update.message.chat.id)
        bot.sendMessage(update.message.chat_id, text='又見面了呢！')
    except:
        search_id = User.objects.create(telegram_id=update.message.chat.id,
                                        first_name=str(update.message.chat.first_name),
                                        last_name=str(update.message.chat.last_name),
                                        username=str(update.message.chat.username))
        bot.sendMessage(update.message.chat_id, text='是第一次見面呢！不過沒關係，我已經記住你的長相了！')



def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='幹!')

def uva_enroll(bot, update):
    try:
        search_id = User.objects.get(telegram_id=update.message.chat.id)
        print(search_id.username)
        print(search_id.uva_id)
        if search_id.uva_id.strip() != "":
            bot.sendMessage(update.message.chat_id, text='嗨!我還記得你,你最後跟我說的uva帳號是'+search_id.uva_id)
        else:
            bot.sendMessage(update.message.chat_id, text='嗨!你好像沒有跟我說過uva帳號呢')
    except:
        bot.sendMessage(update.message.chat_id, text='你好像沒有透過/start讓我認識你呢!!')


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
    dp.add_handler(CommandHandler("uva", uva_enroll))
    dp.add_handler(CommandHandler("getFile", getFile))
    # on noncommand i.e message - echo the message on Telegram

    dp.add_handler(MessageHandler(Filters.document, getFile))
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

