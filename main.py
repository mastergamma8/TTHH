# -*- coding: utf-8 -*-
from flask import Flask, request
import telegram
import time

app = Flask(__name__)

# Замените YOUR_TOKEN на токен вашего бота
bot = telegram.Bot(token='YOUR_TOKEN')

admin_ids = [12345678]  # Замените на ID администраторов

@app.route('/' + 'YOUR_TOKEN', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id

    # Пример команд модерации
    if update.message.text == '/start':
        bot.sendMessage(chat_id, "Привет! Я бот-модератор.")
    
    elif update.message.text.startswith('/ban'):
        # Логика для бана пользователя
        if user_id in admin_ids:
            banned_user_id = update.message.text.split()[1]
            bot.kickChatMember(chat_id, banned_user_id)
            bot.sendMessage(chat_id, "Пользователь {} был забанен.".format(banned_user_id))
        else:
            bot.sendMessage(chat_id, "У вас нет прав для выполнения этой команды.")

    elif update.message.text.startswith('/mute'):
        # Логика для мьюта пользователя
        if user_id in admin_ids:
            muted_user_id = update.message.text.split()[1]
            bot.restrictChatMember(chat_id, muted_user_id, until_date=int(time.time() + 3600), can_send_messages=False)
            bot.sendMessage(chat_id, "Пользователь {} был замучен на 1 час.".format(muted_user_id))
        else:
            bot.sendMessage(chat_id, "У вас нет прав для выполнения этой команды.")
    
    return 'ok'

@app.route('/')
def index():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(port=5000)
