import telebot
import pickle
import random
from tokenizer import custom_tokenizer

TOKEN = "secret token"
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


bot.delete_webhook()
bot.polling(none_stop=True)
