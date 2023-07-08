from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from telebot import custom_filters
from base import Database

token = '5810757853:AAF7dCjAOtva77wl9_gg_WCx5tnomI_GJSc'

bot = telebot.TeleBot(token)

db = Database('db.db')


@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton('👥 Поиск собеседника')
    markup.add(button_1)
    bot.reply_to(message, 'Привет ' + message.from_user.username + '! Добро пожаловать в Анонимный чат!',reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton('👥 Поиск собеседника')
    button_2 = KeyboardButton('Поистк по полу')
    markup.add(button_1, button_2)
    bot.reply_to(message, '📔 Меню', reply_markup= markup)

@bot.message_handler(commands=['next'])
def next(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton('❌ Остановить поиск')
    markup.add(button_1)

    chat_two = db.get_chat()

    if db.create_chat(message.chat.id, chat_two) == False:
        db.add_queue(message.chat.id, message.from_user.username)
        bot.reply_to(message, '👥 Поиск собеседника...', reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton('/stop')
        button_2 = KeyboardButton('/next')
        markup.add(button_1, button_2)
        b = 'Собеседник найден! Чтобы остановить диалог, напишите /stop \n Что бы найти нового собеседника, напишите /next'
        bot.send_message(message.chat.id, b, reply_markup=markup)
        bot.send_message(chat_two, b, reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton('👥 Поиск собеседника')
        markup.add(button_1)

        bot.send_message(chat_info[1], '❌ Собеседник покинул чат', reply_markup=markup)
        bot.send_message(message.chat.id, '❌ Вы вышли из чата', reply_markup=markup)

    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = KeyboardButton('👥 Поиск собеседника')
        markup.add(button_1)
        bot.send_message(message.chat.id, '❌ Вы не начали чат!', reply_markup=markup)


@bot.message_handler(content_types= ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Поиск собеседника':
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            button_1 = KeyboardButton('❌ Остановить поиск')
            markup.add(button_1)

            chat_two = db.get_chat()


            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, message.from_user.username)
                bot.reply_to(message, '👥 Поиск собеседника', reply_markup=markup)
            else:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                button_1 = KeyboardButton('/stop')
                markup.add(button_1)
                b = 'Собеседник найден! Чтобы остановить диалог, напишите /stop \n Что бы найти нового собеседника, напишите /next'
                bot.send_message(message.chat.id, b, reply_markup=markup)
                bot.send_message(chat_two, b, reply_markup=markup)

        elif message.text == '❌ Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.reply_to(message, '❌ Поиск остановлен, нажмите /menu')

        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)


'''
❌📔👥🔍🔎➿♣️♠️
'''

bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())
bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()