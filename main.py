import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

with open('url_photos.txt', 'r') as f:
    photos = f.readlines()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Мяу мур")
    keyboard = types.InlineKeyboardMarkup()
    key_randomPhoto = types.InlineKeyboardButton(text='Рандом фото', callback_data='randomPhoto')
    keyboard.add(key_randomPhoto)
    bot.send_message(message.chat.id, 'Выбери что нужно сделать:', reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, 'Нажми /start')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'randomPhoto':
        random_index = random.randint(0, len(photos) - 1)
        bot.send_photo(call.message.chat.id, photos[random_index])
        keyboard = types.InlineKeyboardMarkup()
        key_randomPhoto = types.InlineKeyboardButton(text='Да!', callback_data='randomPhoto')
        keyboard.add(key_randomPhoto)
        bot.send_message(call.message.chat.id, 'Хочешь еще?', reply_markup=keyboard)


bot.infinity_polling()
