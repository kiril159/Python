import telebot
from telebot import types
import requests

first_id = str()
second_id = str()
action = str
bot = telebot.TeleBot('5444414945:AAE8X9rNiQl7avGoRoknkBxgI-jtAU3nUEo')

@bot.message_handler(commands=['start'])
def get_text_messages(message):
    keyboard = types.InlineKeyboardMarkup()
    key_first = types.InlineKeyboardButton(text='Эпик из Redmine в Jira', callback_data='first')
    keyboard.add(key_first)
    key_second = types.InlineKeyboardButton(text='Эпик из Jira в Redmine ', callback_data='second')
    keyboard.add(key_second)
    key_third = types.InlineKeyboardButton(text='Задачу из Redmine в Jira', callback_data='third')
    keyboard.add(key_third)
    key_fourth = types.InlineKeyboardButton(text='Задачу из Jira в Redmine', callback_data='fourth')
    keyboard.add(key_fourth)
    bot.send_message(message.from_user.id, text='Выбери действие:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global action
    action = call.data
    if call.data == "first":
        msg = f'Введите оба ID эпика в формате Redmine_ID:Jira_ID :'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "second":
        msg = f'Введите оба ID эпика в формате Jira_ID:Redmine_ID :'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "third":
        msg = f'Введите оба ID задачи в формате Redmine_ID:Jira_ID :'
        bot.send_message(call.message.chat.id, msg)
    else:
        msg = f'Введите оба ID задачи в формате Jira_ID:Redmine_ID :'
        bot.send_message(call.message.chat.id, msg)


@bot.message_handler(content_types=['text'])
def get_first(message):
    global first_id, second_id
    lists = message.text.split(":")
    first_id = lists[0]
    second_id = lists[1]
    try:
        if action == "first":
            data = {
                "id_redmine": first_id,
                "id_jira": second_id
            }
            requests.post('http://127.0.0.1:8000/epic_red_to_jira', json=data)
            msg = "added epic in Jira "
        elif action == "second":
            data = {
                "id_jira": first_id,
                "id_redmine": second_id
            }
            requests.post('http://127.0.0.1:8000/epic_jira_to_red', json=data)
            msg = "added epic in Redmine "
        elif action == "third":
            data = {
                "id_redmine": first_id,
                "id_jira": second_id
            }
            requests.post('http://127.0.0.1:8000/task_red_to_jira', json=data)
            msg = "added task in Jira "
        else:
            data = {
                "id_jira": first_id,
                "id_redmine": second_id
            }
            requests.post('http://127.0.0.1:8000/task_jira_to_red', json=data)
            msg = "added task in Redmine "
    except:
        msg = 'Incorrect value'
    bot.send_message(message.from_user.id, text=msg)


bot.polling(none_stop=True, interval=0)
