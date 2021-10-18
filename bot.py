import telebot
import pickle
from tokenizer import custom_tokenizer

TOKEN = "2058390751:AAHhvKBSTKvYHISU7upPkdLfEg5sJcftu38"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_sticker(msg.chat.id, 'CAACAgIAAxkBAAEDGaZhayQAAWkV0aApRRYh6tWVZqmGAmIAAhoCAAJcKIYIg-9zfYvSQlQhBA')


@bot.message_handler(content_types=['text'])
def echo_message(msg):
    clf = pickle.load(open('pretrained_clf', 'rb'))
    vectorizer = pickle.load(open('pretrained_vect', 'rb'))
    if clf.predict(vectorizer.transform([msg.text]))[0] == 1:
        bot.delete_message(msg.chat.id, msg.id)


bot.polling(none_stop=True)
