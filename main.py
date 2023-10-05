import telebot
from telebot import types
import json
import time
from datetime import datetime
import Parsing

TOKEN = "6504422834:AAELkmoqRG2PC_ZzOpPcovUWsTqyetBYbOs"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup()
        btn2 = types.KeyboardButton('Расписание электричек')
        markup.row(btn2)
        bot.send_message(message.chat.id, f"Привет, {message.chat.username}", reply_markup=markup)
        bot.register_next_step_handler(message, on_click)
    else:
        bot.send_message(message.chat.id, f"<b>Документация бота:</b>\n1. Бот в разработке\n"
                                          f"2. Бот в разработке\n"
                                          f"3. Бот в разработке", parse_mode='html')



def on_click(message):
    if message.text == 'Расписание занятий':
        markup = types.ReplyKeyboardMarkup()
        btn3 = types.KeyboardButton('РУТ МИИТ')
        btn4 = types.KeyboardButton('МГТУ')
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, f"Выберите учебное заведение, {message.chat.username}", reply_markup=markup)
    elif message.text == 'Расписание электричек':
        markup = types.ReplyKeyboardMarkup()
        btn5 = types.KeyboardButton('Бужаниново - Москва')
        btn6 = types.KeyboardButton('Москва - Бужаниново')
        markup.row(btn5, btn6)
        bot.send_message(message.chat.id, f"Куда поедем, {message.chat.username}?", reply_markup=markup)
        bot.register_next_step_handler(message, elektrich)


@bot.message_handler(content_types=['text'])
def elektrich(message):
    if message.text == 'Бужаниново - Москва':
        markup = types.ReplyKeyboardMarkup()
        btn7 = types.KeyboardButton('Посмотреть данные Б-М')
        markup.row(btn7)
        bot.send_message(message.chat.id, f"Выбери электричку, {message.chat.username}!",
                         reply_markup=markup)
        bot.register_next_step_handler(message, get_dan)
    elif message.text == 'Москва - Бужаниново':
        markup = types.ReplyKeyboardMarkup()
        btn7 = types.KeyboardButton('Посмотреть данные М-Б')
        markup.row(btn7)
        bot.send_message(message.chat.id, f"Выбери электричку, {message.chat.username}!",
                         reply_markup=markup)
        bot.register_next_step_handler(message, get_dan)



@bot.message_handler(content_types=['text'])
def get_dan(message):
    if message.text == 'Посмотреть данные Б-М':
        Parsing.main()
        markup = types.ReplyKeyboardMarkup()
        with open("tutu.json", 'r', encoding='utf-8') as file:
            trains = json.load(file)
        bot.send_message(message.chat.id, f"Время отправления: {trains['1']['start_time']}\n"
                                          f"Время прибытия: {trains['1']['end_time']}\n"
                                          f"График: {trains['1']['movement']}\n"
                                          f"Время в пути: {trains['2']['time_in_road']}\n"
                                          f"Маршрут: {trains['1']['way']}", reply_markup=markup)

    elif message.text == 'Посмотреть данные М-Б':
        Parsing.main()
        markup = types.ReplyKeyboardMarkup()
        with open("tutu.json", 'r', encoding='utf-8') as file:
            trains = json.load(file)

        for key in trains:
            bot.send_message(message.chat.id, f"Время отправления: {trains[key]['start_time']}\n"
                                              f"Время прибытия: {trains[key]['end_time']}\n"
                                              f"График: {trains[key]['movement']}\n"
                                              f"Время в пути: {trains[key]['time_in_road']}\n"
                                              f"Маршрут: {trains[key]['way']}", reply_markup=markup)
            time.sleep(1)



bot.polling(none_stop=True)
