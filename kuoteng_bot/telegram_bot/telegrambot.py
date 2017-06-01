#_*_ encoding: utf-8 _*_
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InlineQueryResultLocation
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from django_telegrambot.apps import DjangoTelegramBot
from emoji import emojize
#uva upload function
from telegram_bot import uva
import requests
import requests.packages.urllib3
import json
#word2vec
#不該在此引入...不過分開來做load好像不太優
from gensim.models import word2vec
from gensim import models
from gensim.models.keyedvectors import KeyedVectors

#jieba
import jieba
import random
import jieba.posseg as pseg

#database
from telegram_bot.models import User


import logging
logger = logging.getLogger(__name__)

# from .fsm import TocMachine
from telegram_bot.fsm import machine 

import pprint
pp = pprint.PrettyPrinter(indent=4)

# word2vec load

PUNCTUATIONS = [',','.',':',';','?','!','(',')','[',']','@','&','#','%','$','{','}','--','-','？', '！', '。'
                , ' ']

logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)
model = KeyedVectors.load_word2vec_format("med250.model.bin", binary=True)

jieba.set_dictionary('jieba_data/dict.txt.big')

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

WEATHER_API_ID = 'b1b15e88fa797225412429c1c50c122a1'
WEATHER_API = 'http://samples.openweathermap.org/data/2.5/forecast'
ANSWER = ['你是不是想說','你是想要聊','不知道你的意思是不是','我想你應該是想要聊','聽起來是']
ANSWER2 = ['原來如此, 但我不太懂你想說什麼呢','我的理解力不夠...','阿哈哈佐佑理不知道']

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
    
    keyboard = [[InlineKeyboardButton("(重新)設定uva帳號", callback_data='1'),
                 InlineKeyboardButton("(重新)設定uva密碼", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(update.message.chat_id, text='點選以下按鈕讓我更加認識你<3', reply_markup=reply_markup)

def button(bot, update):
    print(update)
    try:
        search_id = User.objects.get(telegram_id=update.callback_query.message.chat.id)
        query = update.callback_query
        if query.data == '1':
            bot.sendMessage(update.callback_query.message.chat.id, text='那麼, 請告訴我你的帳號(Tips:任何下一次輸入字串都視為帳號)')
            search_id.states = 1
            search_id.save()
        else:
            bot.sendMessage(update.callback_query.message.chat.id, text='那麼, 請告訴我你的密碼(Tips:任何下一次輸入字串都視為密碼)')
            search_id.states = 2
            search_id.save()
    except:
        bot.sendMessage(update.callback_query.message.chat.id, text='你還沒有透過/start讓我認識你呢! 做事要按照優先順序呀QQ')

def help(bot, update):
    update.message.reply_text('kuoteng_bot:國騰機器人')
    bot.sendPhoto(update.message.chat_id, photo='https://telegram.org/img/t_logo.png')
    bot.sendMessage(update.message.chat_id, text="/fsm:印出fsm")
    bot.sendMessage(update.message.chat_id, text="/uva:查看綁訂uva帳戶")
    bot.sendMessage(update.message.chat_id, text="/start:更新用戶資訊")
    bot.sendMessage(update.message.chat_id, text="_直接上傳檔案_:uva上傳",parse_mode=ParseMode.MARKDOWN)
    bot.sendMessage(update.message.chat_id, text="_跟我聊天_:我跟你聊天",parse_mode=ParseMode.MARKDOWN)
    bot.sendMessage(update.message.chat_id, text="_直接給我地點_:查看當地天氣預報",parse_mode=ParseMode.MARKDOWN)
    bot.sendMessage(update.message.chat_id, text="_給我貼圖_:回敬你一樣的貼圖",parse_mode=ParseMode.MARKDOWN)

    bot.sendSticker(update.message.chat.id, sticker = "CAADBQADIAUAAmQK4AU1xVFZqAVROQI")

    bot.sendMessage(update.message.chat_id, text="烏丸賽高")
def uva_enroll(bot, update):
    try:
        search_id = User.objects.get(telegram_id=update.message.chat.id)
        print(search_id.username)
        print(search_id.uva_id)
        if search_id.states > -1:
            bot.sendMessage(update.message.chat_id, text='嗨!我還記得你,你最後跟我說的uva帳號是'+search_id.uva_id)
        else:
            bot.sendMessage(update.message.chat_id, text='嗨!你好像沒有跟我說過uva帳號呢')
    except:
        bot.sendMessage(update.message.chat_id, text='你好像沒有透過/start讓我認識你呢!!')


def echo(bot, update):
    try:
        search_id = User.objects.get(telegram_id=update.message.chat_id)
        if search_id.states == 1:
            search_id.uva_id = update.message.text
            logger.info("set the uva_id to %s" % (update.message.text))
            search_id.states = 0
            search_id.save()
            return
        elif search_id.states == 2:
            search_id.uva_passwd = update.message.text
            logger.info("set the uva_passwd")
            search_id.states = 0
            search_id.save()
            return
        else:
            print(search_id)
            print(search_id.states)
            pass
    except:
        logger.info("this person has not used the /start")

    msg = pseg.cut(update.message.text)
    #print(msg)
    #pp.pprint(msg)
    nword_list = []
    for word,flag in msg:
        if word not in PUNCTUATIONS:
            print(word,flag)
            if flag.find('n') != -1:
                nword_list.append(str(word))
            elif flag.find('b') != -1:
                nword_list.append(str(word))
            elif flag.find('x') != -1:
                nword_list.append(str(word))
    print(nword_list)
    try:
        index = random.randint(0, len(nword_list)-1)
        print(nword_list[index])
        res = model.most_similar(nword_list[index], topn = 10)
        item_index = random.randint(0, len(res)-1)
        answer_index = random.randint(0, len(ANSWER)-1)
        bot.sendMessage(update.message.chat_id, text='這好像跟'
                                                +nword_list[index]+'有關')
        bot.sendMessage(update.message.chat_id, text=ANSWER[answer_index]+res[item_index][0]+'的話題嗎?')
    except:
        index = random.randint(0, len(ANSWER2)-1)
        bot.sendMessage(update.message.chat_id, text=ANSWER2[index])

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
    try:
        search_id = User.objects.get(telegram_id=update.message.chat.id)
        uva_id = search_id.uva_id
        uva_passwd = search_id.uva_passwd
        file = bot.getFile(update.message.document.file_id)
        file_name = update.message.document.file_name
        number = int(file_name.strip(".cpp").strip('UVA-'))
        
        code = requests.get(file.file_path).content
        bot.sendMessage(update.message.chat_id,
                        text="```"+str(code)+"```",
                        parse_mode=ParseMode.MARKDOWN)
        submission = uva.submit(uva_id,uva_passwd,number,file.file_path)
        if submission == True:
            bot.sendMessage(update.message.chat_id, text='%s 已經上傳' % file_name)
        else:
            bot.sendMessage(update.message.chat_id, text='好像有點錯誤！')
    except:
        bot.sendMessage(update.message.chat_id, text='我不記得你有告訴過我你的uva帳號!')

def location(bot, update):
    print(update)
    payload = {
                'lat': int(update.message.location.longitude),
                'lon': int(update.message.location.latitude),
                'appid': WEATHER_API_ID
            }
    try:
        res = requests.get(WEATHER_API, params=payload)
        print(res)
        print(res.text)
        weather = json.loads(res.text)
        pp.pprint(weather)

        bot.sendMessage(update.message.chat.id, text='根據你傳過來的地點!!我判斷UTC '\
                                    + weather['list'][0]['dt_txt'] + '的天氣是...')
        bot.sendMessage(update.message.chat.id, text=weather['list'][0]['weather'][0]['description'] \
                                    + '溫度(F): '+ str(weather['list'][0]['main']['temp']) + 
                                    '濕度(%): ' + str(weather['list'][0]['main']['humidity'])+ 
                                    '風速: ' + str(weather['list'][0]['wind']['speed']))
    except:

        bot.sendMessage(update.message.chat.id, text='天氣API好像抽風了...請稍後再試')


def sticker(bot, update):
    bot.sendSticker(update.message.chat.id, sticker = update.message.sticker.file_id)

def main():

    logger.info("Loading handlers for telegram bot")
    dp = DjangoTelegramBot.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("fsm", nowDiagram))
    dp.add_handler(CommandHandler("uva", uva_enroll))
    dp.add_handler(CommandHandler("getFile", getFile))
    dp.add_handler(CallbackQueryHandler(button))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.location, location))
    dp.add_handler(MessageHandler(Filters.document, getFile))
    dp.add_handler(MessageHandler([Filters.text], echo))
    dp.add_handler(MessageHandler(Filters.sticker, sticker))

    # log all errors
    dp.add_error_handler(error)

if __name__ == "__main__":
    pass
