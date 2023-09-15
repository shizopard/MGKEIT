import telebot
from telebot import types
import datetime
import json
import pytz  

moscow_tz = pytz.timezone('Europe/Moscow')
bot = telebot.TeleBot(' ')

# JSON
def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка при декодировании JSON в файле {filename}.")
        return None

def get_moscow_time():
    return datetime.datetime.now(moscow_tz)

nowDay = get_moscow_time().weekday()
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
nowDay = days_of_week[nowDay]

current_date = get_moscow_time()
week_number = current_date.isocalendar()[1]
if week_number % 2 == 0:
    nowParity = "Четная неделя"
else:
    nowParity = "Нечетная неделя"

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        relist = types.KeyboardButton("🗓️ Замены")
        list = types.KeyboardButton("🗓️ Расписание")
        dayInfo = types.KeyboardButton("📋 День")
        help = types.KeyboardButton("⚠️ Помощь")
        settings = types.KeyboardButton("⚙️ Функции")
        keyboard.add(relist, list, dayInfo, help, settings)
        bot.send_message(message.chat.id, "Привет! Навигация по боту:\n🗓️ Замены - список замен\n🗓️ Расписание - расписание на день\n📋 День - информация о текущем дне\n⚠️ Помощь - помощь по боту", reply_markup=keyboard)
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /start")


    # Команды в меню из кнопок 

    elif message.text == "🗓️ Расписание":
        filename = "couples.json"
        parsed_data = read_json_file(filename)
        if parsed_data:
            try:
                monday_schedule = parsed_data[nowParity][nowDay]
                text_schedule = ""
                for key, value in monday_schedule.items():
                    text_schedule += f"{key}: {value}\n"
                bot.send_message(message.chat.id, f"Расписание на {nowDay}:\n\n{text_schedule}")
                print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Расписание")
            except KeyError:
                print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")
                print(f"[{datetime.datetime.now()}] Данные о расписании на день не были получены, ошибка")

    elif message.text == "🗓️ Замены":
        bot.send_message(message.chat.id, f"Функция в разработке")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")

    elif message.text == "⚠️ Помощь":
        bot.send_message(message.chat.id, "Бот создан для группы 1ИП-4-23\nСписок основных возможностей:\n- Просмотр расписания на текущий день.\n- Просмотр замен на текущий день.\n- Просмотр основной информации на день.")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Помощь")

    elif message.text == "⚙️ Функции":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        addList = types.KeyboardButton("✅ Рассылка")
        remList = types.KeyboardButton("❌ Рассылка")
        skipList = types.KeyboardButton("")
        reminder = types.KeyboardButton("✅ Напоминания")
        offReminder = types.KeyboardButton("❌ Напоминания")
        chatInfo = types.KeyboardButton("📋 О чате")
        keyboard.add(addList, remList, skipList, reminder, offReminder, skipList, chatInfo)
        bot.send_message(message.chat.id, f"Список основных функций в боте:\n- Добавление чата в рассылку бота\n- Удаление чата из рассылки\n- Установка напоминания о парах", reply_markup=keyboard)
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду День")

    # Команды для отладки

    elif message.text == "/getid":
        bot.send_message(message.chat.id, f"ID чата: {message.chat.id}")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /getid")

    elif message.text == "/debug":
        bot.send_message(message.chat.id, f"Дебаг-информация:\nChat ID: {message.chat.id}\n\nИнформация о пользователе:\nUID: {message.from_user.id}\nUNAME: {message.from_user.username}")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /debug")


bot.polling(none_stop=True, interval=0)


# Коды ошибок
# 1 - начинающиеся на 1, ошибки связанные с бэк
# 100 - Дата не была определена
# 101 - Команда не найдена
# 102 - Не удалосьп загрузить данные

# 2 - начинающиеся на 2, проблемы со стороны пользователя
# 200 - Доступ запрещен
# 201 - Пользователь заблокирован
# 202 - Неверный код авторизации

# Для реализации в будущем:

#TODO: Список замен, который автоматически берется из .pdf файла на сайте колледжа
#TODO: Автоматическая отправка уведомления о следующей паре в конце каждой пары
#TODO: Автоматическая отправка уведомления о текущем дне недели в 07:30
#TODO: Уведомления могут отправляться в определенные чаты, которые сохраняются в .json файл. Добавить чат в список для уведомлений можно будет при помощи команды
#TODO: Подписка на уведомления о парах в личные сообщения бота
#TODO: Сделать более чистое расписание, всё в одну строку

# Для исправления
