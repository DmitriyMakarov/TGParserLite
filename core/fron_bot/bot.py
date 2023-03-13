import asyncio

import telebot
import configparser
from core.helpers import mysql


from core.helpers import users_db, db

config = configparser.ConfigParser()
config.read('../../res/config/config.ini')
config.sections()

apy_key = config['TG']['api_key']
print(apy_key)
bot = telebot.TeleBot(apy_key, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message.chat.id)
    if mysql.check_user_exist(message.chat.id) == 0:
        mysql.add_user(message.chat.id)
    else:
        pass
    bot.reply_to(message, "Howdy, how are you doing?")



bot.infinity_polling()