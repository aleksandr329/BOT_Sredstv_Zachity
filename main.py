import time
import os
import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot import types
from threading import Timer
from parametrs import *
from db import *
from logics import *


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


class MyStates(StatesGroup):# экземпляры класса для создания переменных
    zagolovok = State()
    text = State()
    age = State()

@bot.message_handler(commands=['start'])
def start(message):
    us = message.from_user.id# данные пользователя
    name = message.from_user.first_name
    fam = message.from_user.last_name
    nik = message.from_user.username

    if message.from_user.id in meneger or message.from_user.id in driver or message.from_user.id in admin:# проверка есть ли пользователь в списках
        db_table_val(us, name, fam, nik)# запись данных пользователя
        text = f'{message.from_user.first_name} Добро пожаловать! Выберите действие что вы хотите сделать!'
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton(text='Инструкция пользования', callback_data='instruction'))
        markup.add(telebot.types.InlineKeyboardButton(text='Посмотреть все задания', callback_data='zad_all'))
        markup.add(telebot.types.InlineKeyboardButton(text='Добавить задание', callback_data='go'))
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать задание', callback_data='vibor'))
        markup.add(telebot.types.InlineKeyboardButton(text='Удалить задание', callback_data='delet'))
        markup.add(telebot.types.InlineKeyboardButton(text='Архивные записи', callback_data='period'))
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(msg, step2)

    elif message.chat.id in meneger or message.chat.id in driver or message.chat.id in admin:# это для того когда пользователь попадает в команду старт из инлайнового режима
        text = f'{message.chat.first_name} Добро пожаловать! Выберите действие что вы хотите сделать!'
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(telebot.types.InlineKeyboardButton(text='Инструкция пользования', callback_data='instruction'))
        markup.add(telebot.types.InlineKeyboardButton(text='Посмотреть все задания', callback_data='zad_all'))
        markup.add(telebot.types.InlineKeyboardButton(text='Добавить задание', callback_data='go'))
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать задание', callback_data='vibor'))
        markup.add(telebot.types.InlineKeyboardButton(text='Удалить задание', callback_data='delet'))
        markup.add(telebot.types.InlineKeyboardButton(text='Архивные записи', callback_data='period'))
        msg = bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(msg, step2)

    else:
        db_table_user_without_access(us, name, fam, nik)# запись данных пользователя которого нет в списках
        bot.send_message(message.chat.id, 'У вас нет доступа \nОбратитесь к администратору')
        video = open('video_ne_proydech.MP4', 'rb')
        bot.send_video(message.chat.id, video)


@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    step3(call)# функция для работы с инлайновыми кнопками


@bot.message_handler(content_types= ['photo'])# функция для запуска записи когда user скинет фото
def stasyc(message):
    Timer(300, delite_file).start()# запускаетя таймер чтобы удалить файл если пользователь не будет вводить данные
    bot.send_message(message.chat.id, 'Фото загруженно удачно.')
    bot.set_state(message.from_user.id, MyStates.zagolovok, message.chat.id)
    bot.send_message(message.chat.id, 'Введите название заголовка!')
    with open('1.txt', 'w') as file:# запись фото в файл
        file.write(message.photo[0].file_id)


@bot.message_handler(state=MyStates.zagolovok)
def name_get(message):

    bot.set_state(message.from_user.id, MyStates.text, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['zag'] = message.text.replace('"', '_').replace("'", "_").replace('<','_').replace('>','_').replace('«','_').replace('»','_').replace('*','_').replace('#','_').replace(' ','_').replace('.','_').replace(',','_')
    if len(data['zag']) < 30:
        bot.send_message(message.chat.id, 'Введите комментарий к заданию!')
    else:
        bot.send_message(message.chat.id, 'Вы ввели слишком длинный заголовок. Макс длинна 29 символов')
        delite_file()
        start(message)

@bot.message_handler(state=MyStates.text)
def ask_age(message):
    bot.send_message(message.chat.id, "Введите дату до какого числа нужно это сделать.")
    bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['text'] = message.text.replace('"', ' ').replace("'", " ").replace('<',' ').replace('>',' ').replace('«',' ').replace('»',' ').replace('*',' ').replace('#',' ')


@bot.message_handler(state=MyStates.age)# финальная функция для записи полученных выше данных
def ready_for_answer(message):
    try:
        us = message.from_user.id
        name = message.from_user.first_name
        text = message.text.replace('"', ' ').replace("'", " ").replace('<',' ').replace('>',' ').replace('«',' ').replace('»',' ').replace('*',' ').replace('#',' ')
        if message.from_user.username is None:# если у usera нет nik_name
            nik = bad_name
        else:
            nik = message.from_user.username
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            text_meneger = ("Вот что в итоге получилось:\n<b>"
                    f"Заголовок: {data['zag']}\n"
                    f"Текст: {data['text']}\n"
                    f"До: {text}</b>")
            text_driver = ("У вас новое задание:\n<b>"
                   f"Заголовок: {data['zag']}\n"
                   f"Текст: {data['text']}\n"
                   f"До: {text}</b>")
            with open('1.txt', 'r') as file:
                foto = str(file.read())
            if db_table_get(data['zag']):  # если название заголовка уже существует
                zagolovok = data['zag'] + '✅'
                db_table_zap(zagolovok, data['text'], foto, text, us, name, nik)  # функция для записи задания
                bot.send_message(message.chat.id, text_meneger, parse_mode="html")
                bot.send_photo(message.chat.id, foto)
            else:
                db_table_zap(data['zag'],data['text'], foto, text, us, name, nik)# функция для записи задания
                bot.send_message(message.chat.id, text_meneger, parse_mode="html")
                bot.send_photo(message.chat.id, foto)
            for i in driver:# для рассылки нового задания водителям
                bot.send_message(i, text_driver, parse_mode="html")
                bot.send_photo(i, foto)
        os.remove("1.txt")
        bot.delete_state(message.from_user.id, message.chat.id)
        start(message)
    except FileNotFoundError:# это если пользователь долго вводил задание
        bot.send_message(message.chat.id, helps)
        start(message)



@bot.message_handler()# функция для отлавливания текста от Reply кнопок
def step67(message):
    step4(message)



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())




if __name__ == "__main__":

    try:
        bot.polling(none_stop=True)
    except TimeoutError:
        print('Ошибка')
    finally:
        print('Сработал finally')
        time.sleep(15)
        c = []
        for i in c:
            bot.send_message(i, 'ТелеграмБОТ СРЕДСТВ ЗАЩИТЫ скоро упадет')
        bot.polling(none_stop=True)

