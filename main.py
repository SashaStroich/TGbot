import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("6076831654:AAGOADdBDhDIBqLBpLTRVLyyyiv-Tk2Uc7c")

registered_users = []

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Вітаю! Щоб зареєструватись, натисніть /register.")

@bot.message_handler(commands=['register'])
def register(message):
    chat_id = message.chat.id

    if chat_id in registered_users:
        bot.send_message(chat_id, "Ви вже зареєстровані.")
    else:
        bot.send_message(chat_id, "Введіть ваше прізвище та ініціали:")
        bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text

    if name in registered_users:
        bot.send_message(chat_id, "Це ім'я вже зареєстроване.")
    else:
        registered_users.append(name)
        bot.send_message(chat_id, "Ім'я зареєстровано.")


        markup = types.ReplyKeyboardMarkup(row_width=2)
        service1 = types.KeyboardButton('Заміна паспорту')
        service2 = types.KeyboardButton('Надання адміністративних послуг')
        service3 = types.KeyboardButton('Державна реєстрація шлюбу')
        service4 = types.KeyboardButton('Державна реєстрація народження')
        service5 = types.KeyboardButton('Подача заяви на соціальний захист ')
        service6 = types.KeyboardButton('Подача заяви по Земельних питаннях ')
        markup.add(service1, service2, service3, service4, service5, service6)

        bot.send_message(chat_id, "Оберіть послугу:", reply_markup=markup)
        bot.register_next_step_handler(message, process_service_step)

def process_service_step(message):
    chat_id = message.chat.id
    service = message.text

    bot.send_message(chat_id, "Ви обрали послугу: " + service)
    bot.send_message(chat_id, "Введіть дату у форматі ДД-ММ-РРРР (наприклад, 01-01-2022):")
    bot.register_next_step_handler(message, process_date_step)

def process_date_step(message):
    chat_id = message.chat.id
    date_str = message.text

    try:
        date = datetime.strptime(date_str, "%d-%m-%Y")
        bot.send_message(chat_id, "Ви обрали дату: " + date_str)
        bot.send_message(chat_id, "Введіть час у форматі ГГ:ММ (наприклад, 14:30):")
        bot.register_next_step_handler(message, process_time_step)
    except ValueError:
        bot.send_message(chat_id, "Неправильний формат дати. Спробуйте ще раз.")

def process_time_step(message, date_str=None):
    chat_id = message.chat.id
    time_str = message.text

    try:
        time = datetime.strptime(time_str, "%H:%M").time()
        bot.send_message(chat_id, "Ви обрали час: " + time_str)


        with open('registered_users.txt', 'a') as file:
            file.write(f"Name: {registered_users[-1]}\n")
            file.write(f"Chat ID: {chat_id}\n")
            file.write(f"Date: {date_str}\n")
            file.write(f"Time: {time_str}\n\n")

        bot.send_message(chat_id, "Дякую за реєстрацію!")
        bot.send_message(chat_id, "Ваша заявка успішно оброблена.")
    except ValueError:
        bot.send_message(chat_id, "Неправильний формат часу. Спробуйте ще раз.")

bot.polling()

