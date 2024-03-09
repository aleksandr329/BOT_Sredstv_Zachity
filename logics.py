from main import *
from db import *
from parametrs import *


call_data = []# создаем этот список для того чтобы использовать его значения в разных функциях


def step3(call):
    try:
        list_call_data = [i[1] for i in db_table_all()]# генерим этот список для того чтобы были в нем все заголовки
        if call.data == 'go':
            file = open('1.txt', 'r')# нужно для того чтобы если кто то уже создает задание возникла ошибка
            bot.send_message(call.message.chat.id, stop)
            start(call.message)


        if call.data == 'zad_all':# выводим все задания пользователю
            for i in db_table_all():
                if i[8] in bad_name:# если нет ник нэйма
                    text = f'''
<b>Заголовок</b>: {i[1]}
<b>Основной текст</b>: {i[2]}
<b>Крайний срок</b>: {i[4]}
<b>Дата создания</b>: {i[5]}
<b>Автор</b>: {i[7]}
<b>Автору нужно создать NIK_NAME</b> 😡'''
                else:
                    text = f'''
<b>Заголовок</b>: {i[1]}
<b>Основной текст</b>: {i[2]}
<b>Крайний срок</b>: {i[4]}
<b>Дата создания</b>: {i[5]}
<b>Автор</b>: {i[7]}
<b>Перейти на страницу автора</b>: https://t.me/{i[8]}'''
                bot.send_message(call.message.chat.id, text, parse_mode='HTML')
                bot.send_photo(call.message.chat.id, i[3])
                bot.send_message(call.message.chat.id, '❗❗❗❗❗❗❗❗❗❗❗❗❗❗')
            else:
                start(call.message)


        if call.data == 'vibor':# для вывода заданий в виде кнопок
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttons = []
            for i in db_table_all():
                button = types.KeyboardButton(text=f'{i[1]}')
                buttons.append(button)

            markup.add(*buttons)
            bot.send_message(call.message.chat.id, '👇🏻', reply_markup=markup)

        if call.data == 'delet':# для удаления задания
            if call.message.chat.id in driver:# если пользователь есть в этом списке
                markup = telebot.types.InlineKeyboardMarkup(row_width=1)
                buttons = []
                for i in db_table_all():
                    button = telebot.types.InlineKeyboardButton(text=f'{i[1][:12]}', callback_data=f'{i[1]}')
                    buttons.append(button)

                markup.add(*buttons)
                bot.send_message(call.message.chat.id, '👇🏻', reply_markup=markup)
            else:
                bot.send_message(call.message.chat.id, 'У вас нет доступа')
                video = open('video_ne_proydech.MP4', 'rb')
                bot.send_video(call.message.chat.id, video)
                time.sleep(5)
                start(call.message)


        if call.data in list_call_data:# вот для чего мы генерили список со всеми заголовками наверху
            call_data.append(call.data)# записываем значение в переменную в самом начале
            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            markup.add(telebot.types.InlineKeyboardButton(text='Да удаляем 😎', callback_data='yes'))
            markup.add(telebot.types.InlineKeyboardButton(text='Нет, отменить удаление 😰', callback_data='no'))
            bot.send_message(call.message.chat.id, f'{call.message.chat.first_name} вы уверенны что хотите удалить \n {call_data[-1]} ❓', reply_markup=markup, parse_mode='HTML')

        if call.data == 'yes':
            li_st = db_table_get(call_data[-1])# получаем все значения из таблицы
            db_table_zap2(li_st[1], li_st[2], li_st[6],li_st[7], li_st[8],li_st[3],li_st[5], li_st[4])
            bot.send_message(li_st[6], f'Ваше задание: {li_st[1]} \nВыполнено: {a_time}')
            bot.send_photo(li_st[6], li_st[3])
            db_table_delete(call_data[-1])
            bot.send_message(call.message.chat.id, f'{call_data[-1]} удален ☠')
            start(call.message)

        if call.data == 'no':
            start(call.message)

        if call.data == 'instruction':
            bot.send_message(call.message.chat.id, instruction, parse_mode='HTML')
            bot.send_message(call.message.chat.id, '🤖')
            start(call.message)

        if call.data == 'period':# предлагаем выбрать дату при помощи инлайновых кнопок
            markup = telebot.types.InlineKeyboardMarkup(row_width=8)
            buttons = []
            for i in data_perriod:
                button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                buttons.append(button)
            markup.add(*buttons)
            bot.send_message(call.message.chat.id, 'Выберите дату с какого периода хотите запросить архив', reply_markup=markup)

        if call.data in data_perriod:# если есть совпадения из списка дат
            try:
                file = open('2.txt', 'r')# вызываем ошибку если это первая запись и такого файла нет
                with open('2.txt', 'a') as file:  # запись даты в файл
                    file.write(' '+call.data)
                markup = telebot.types.InlineKeyboardMarkup(row_width=3)
                buttons = []
                for i in mesiac_perriod:
                    button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                    buttons.append(button)
                markup.add(*buttons)
                bot.send_message(call.message.chat.id, 'Выберите месяц до какого периода хотите запросить архив', reply_markup=markup)
            except FileNotFoundError:
                with open('2.txt', 'w') as file:  # запись даты в файл самая первая
                    file.write(call.data)
                Timer(120, delite_file_arhive).start()
                markup = telebot.types.InlineKeyboardMarkup(row_width=3)
                buttons = []
                for i in mesiac_perriod:
                    button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                    buttons.append(button)
                markup.add(*buttons)
                bot.send_message(call.message.chat.id, 'Выберите месяц с какого периода хотите запросить архив', reply_markup=markup)

        if call.data in mesiac_perriod:# если есть совпадения из списка месяцев
            try:
                file = ''
                with open('2.txt', 'r') as file1:# это для того чтобы понять какой идет период с или до
                    for i in file1:
                        file = file + i

                if len(file) == 2:# если это первая запись с какого периода
                    with open('2.txt', 'a') as file:  # запись месяца в файл
                        file.write('-'+call.data)
                        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
                        buttons = []
                        for i in god_perriod:
                            button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                            buttons.append(button)
                        markup.add(*buttons)
                        bot.send_message(call.message.chat.id, 'Выберите год с какого периода хотите запросить архив', reply_markup=markup)

                else:
                    with open('2.txt', 'a') as file:  # запись месяца в файл
                        file.write('-'+call.data)
                        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
                        buttons = []
                        for i in god_perriod:
                            button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                            buttons.append(button)
                        markup.add(*buttons)
                        bot.send_message(call.message.chat.id, 'Выберите год до какого периода хотите запросить архив', reply_markup=markup)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, 'Что то пошло не так ☹ \n Попробуйте заново')
                start(call.message)


        if call.data in god_perriod:# если есть совпадения из списка годов
            try:
                file_len = ''
                with open('2.txt', 'r') as file:
                    for i in file:
                        file_len = file_len + i
                if len(file_len) < 12:# если это самая первая запись года с какого периода
                    with open('2.txt', 'a') as file:# запись года в файл
                        file.write('-'+call.data)
                    markup = telebot.types.InlineKeyboardMarkup(row_width=8)
                    buttons = []
                    for i in data_perriod:
                        button = telebot.types.InlineKeyboardButton(text=i, callback_data=i)
                        buttons.append(button)
                    markup.add(*buttons)
                    bot.send_message(call.message.chat.id, 'Выберите дату до какого периода хотите запросить архив', reply_markup=markup)

                else:
                    with open('2.txt', 'a') as file: # запись года в файл
                        file.write('-'+call.data)
                    final_list_arhive = db_table_perriod()# сохранняем полученную колекцию из архива в переменную
                    if len(final_list_arhive) == 0:# если список пустой значит пользователь выбрал несуществующий период
                        bot.send_message(call.message.chat.id, 'Вы ввели неправильно даты архива')
                        bot.send_message(call.message.chat.id, '🤯')
                        start(call.message)
                    else:# если все нормально
                        for i in final_list_arhive:
                            text_arhive = f'''
    <b>ЗАПИСЬ ИЗ АРХИВА 📊</b>
    
    <b>ДАТА ВЫПОЛНЕНИЯ ЗАДАНИЯ:</b> {i[8]}
    <b>ЗАГОЛОВОК:</b> {i[1]}
    <b>ТЕКСТ:</b> {i[2]}
    <b>СРОК ВЫПОЛНЕНИЯ:</b> {i[9]}
    <b>ДАТА СОЗДАНИЯ ЗАДАНИЯ:</b> {i[7]}
    <b>АВТОР ЗАДАНИЯ:</b> {i[4]}
    https://t.me/{i[5]}
    '''
                            bot.send_message(call.message.chat.id, '🔴')
                            bot.send_message(call.message.chat.id, text_arhive, parse_mode='HTML')
                            bot.send_photo(call.message.chat.id, i[6])
                        start(call.message)
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, 'Что то пошло не так ☹ \nПопробуйте заново')
                start(call.message)

        else:
            pass

    except AttributeError:
        pass
    except TypeError:
        pass
    except FileNotFoundError:
        if call.message.chat.id in meneger:# проверка есть ли пользователь в списке менеджеров
            bot.send_message(call.message.chat.id, 'Пришлите фото')
        else:
            bot.send_message(call.message.chat.id, 'У вас нет доступа')
            video = open('video_ne_proydech.MP4', 'rb')
            bot.send_video(call.message.chat.id, video)
            time.sleep(5)
            start(call.message)


def step4(message):
    if db_table_get(message.text):# если в таблице есть такой заголовок. Это для отлавливания значения с кнопки
        text = db_table_get(message.text)
        if text[8] in bad_name:# если нет ник нэйма
            text2 = f'''
<b>Заголовок</b>: {text[1]}
<b>Основной текст</b>: {text[2]}
<b>Крайний срок</b>: {text[4]}
<b>Дата создания</b>: {text[5]}
<b>Автор</b>: {text[7]}
<b>Автору нужно создать NIK_NAME</b> 😡'''
        else:
            text2 = f'''
<b>Заголовок</b>: {text[1]}
<b>Основной текст</b>: {text[2]}
<b>Крайний срок</b>: {text[4]}
<b>Дата создания</b>: {text[5]}
<b>Автор</b>: {text[7]}
<b>Перейти на страницу автора</b>: https://t.me/{text[8]}'''
        bot.send_message(message.chat.id, text2, parse_mode='HTML')
        bot.send_photo(message.chat.id, text[3])
        start(message)
    else:
        pass

def delite_file():# это для удаления файла если пользователь долго вводил задание
    try:
        os.remove("1.txt")
    except FileNotFoundError:
        pass

def delite_file_arhive():# это для удаления файла если пользователь долго вводил задание
    try:
        os.remove("2.txt")
    except FileNotFoundError:
        pass
