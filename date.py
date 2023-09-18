import telebot
from telebot import types
import datetime
import json
import pytz  

moscow_tz = pytz.timezone('Europe/Moscow')
bot = telebot.TeleBot('')

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
        help = types.KeyboardButton("⚠️ Помощь")
        resources = types.KeyboardButton("🌐 Ресурсы")
        keyboard.add(relist, list, help, resources)
        bot.send_message(message.chat.id, f"{message.from_user.username}, Привет! Навигация по боту:\n🗓️ Замены - список замен\n🗓️ Расписание - расписание на день\n⚠️ Помощь - помощь по боту", reply_markup=keyboard)
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /start")

    elif message.text == "🗓️ Расписание":
        filename = "couples.json"
        parsed_data = read_json_file(filename)
        if parsed_data:
            try:
                monday_schedule = parsed_data[nowParity][nowDay]
                text_schedule = ""
                for key, value in monday_schedule.items():
                    text_schedule += f"{key}: {value}\n"
                bot.send_message(message.chat.id, f"{message.from_user.username}, Расписание на {nowDay} ({nowParity}):\n\n{text_schedule}")
                print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Расписание")
            except KeyError:
                print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")
                print(f"[{datetime.datetime.now()}] Данные о расписании на день не были получены, ошибка")

    elif message.text == "🗓️ Замены":
        bot.send_message(message.chat.id, f"{message.from_user.username}, Список замен на {nowDay}:\n- Сегодня замен нет")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Замены")

    elif message.text == "⚠️ Помощь":
        bot.send_message(message.chat.id, f"{message.from_user.username}, Бот создан для группы 1ИП-4-23\nСписок основных возможностей:\n- Просмотр расписания на текущий день.\n- Просмотр замен на текущий день.\n- Просмотр основной информации на день.")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду Помощь")

    elif message.text == "🌐 Ресурсы":
        bot.send_message(message.chat.id, f"{message.from_user.username}, ресурсы:\n- Навигатор студента: sites.google.com/view/mgkeitstudent/\n- ВКонтакте: vk.com/mgkeit1\n- Телеграм: t.me/mgkeit\n- Работа от МГКЭИТ: t.me/VacanciMGKEIT")

    elif message.text == "/getid":
        bot.send_message(message.chat.id, f"{message.from_user.username}, ID чата: {message.chat.id}")
        print(f"[{datetime.datetime.now()}] Пользователь {message.from_user.username}[id: {message.from_user.id}] использовал команду /getid")

bot.polling(none_stop=True, interval=0)
