import telebot
import pickle
import random
from flask import Flask, request
import logging
import os
from tokenizer import custom_tokenizer

TOKEN = "2058390751:AAHhvKBSTKvYHISU7upPkdLfEg5sJcftu38"
bot = telebot.TeleBot(TOKEN)

greeting_sticker_id = 'CAACAgIAAxkBAAEDwjFh8ardnzpydiZgMq5T_Hv5YI9WVQACVwEAAhAabSKlKzxU-3o0qiME'
clf = pickle.load(open('model/pretrained_clf', 'rb'))
vectorizer = pickle.load(open('model/pretrained_vect', 'rb'))
th = pickle.load(open('model/threshold', 'rb'))
answers = [
    "Зачем ты говоришь такие вещи?:(",
    "Не будь токсичным",
    "Хватит ругаться",
    "Попрошу не выражаться",
    "Мне пришлось удалить твое сообщение",
    "В этом чате так не принято",
    "Давайте будем жить дружно",
    "Будь вежливее"
]


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_sticker(msg.chat.id, greeting_sticker_id)
    greeting_text = "Чтобы узнать, что со мной делать, отправь команду /help"
    bot.send_message(msg.chat.id, greeting_text)


@bot.message_handler(commands=['help'])
def welcome(msg):
    help_text = "Все очень просто:\n\n" \
                "1. Добавь меня в чат, где нужно следить за недопустимыми сообщениями\n\n" \
                "2. Дай мне права администратора, чтобы я мог удалять сообщения\n\n" \
                "3. Остальная работа на мне!;)"
    bot.send_message(msg.chat.id, help_text)


@bot.message_handler(content_types=['text'])
def echo_message(msg):
    if clf.predict_proba(vectorizer.transform([msg.text]))[:, 1] > th:
        bot.delete_message(msg.chat.id, msg.id)
        bot.send_message(msg.chat.id, random.choice(answers))


if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    app = Flask(__name__)


    @app.route("/bot", methods=['POST'])
    def get_message():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @app.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://toxiccommentsbot.herokuapp.com/")
        return 200
    app.run()
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
