import telebot
from telebot import types
import datetime
import json
import pytz

moscow_tz = pytz.timezone('Europe/Moscow')

bot = telebot.TeleBot('')

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
        list = types.KeyboardButton("🗓️ Расписание")
        keyboard.add(list)
        bot.send_message(message.chat.id, "Привет! Для работы с ботом используй кнопки", reply_markup=keyboard)
    elif message.text == "🗓️ Расписание":
        filename = "couples.json"
        parsed_data = read_json_file(filename)
        if parsed_data:
            try:
                monday_schedule = parsed_data[nowParity][nowDay]
                text_schedule = ""
                for key, value in monday_schedule.items():
                    text_schedule += f"{key}: {value}\n"
                bot.send_message(message.chat.id, text_schedule)
            except KeyError:
                print("Данные не найдены.")

bot.polling(none_stop=True, interval=0)