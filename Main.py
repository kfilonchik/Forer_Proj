import telebot
from random import choice
import random
import datetime
from datetime import date

API_TOKEN = '312164149:AAHGpHx3chsDOQ-dqWwqC_tW-fCf4ukQ6cA'
bot = telebot.TeleBot(API_TOKEN)

horoscope = {}

def getTextFromHoroscope(sign):
    d = date.today()
    if (d, sign) not in horoscope:
        horoscope[(d, sign)] = gen_horoscope()

    return horoscope[(d, sign)]

def prepare_horoscope():
    with open('text.txt', encoding='utf-8') as f:
        global words
        words = []
        words = f.read().split()
    markov_chain = {}
    for i in range(0, len(words) - 2):
        key = (words[i], words[i+1])
        markov_chain.setdefault(key, [])
        markov_chain[key].append(words[i+2])
    return markov_chain

def gen_horoscope():
    stopsentence = (".", "!", "?",)
    markov_chain = prepare_horoscope()
    size = 25
    gen_words = []
    seed = random.randint(0, len(words) - 3)
    w1 = words[seed]
    while (w1.isupper()  or w1.islower()):
        seed = random.randint(0, len(words) - 3)
        w1 = words[seed]
    w2 = words[seed+1]

    for i in range(0, size-1):
        gen_words.append(w1)
        try:
            w3 = choice(markov_chain[(w1,w2)])
        except KeyError:
            break
        w1, w2 = w2, w3

    while True:
        gen_words.append(w1)
        if w1[-1] in stopsentence:
             break
        try:
            w3 = choice(markov_chain[(w1,w2)])
        except KeyError:
            break
        w1, w2 = w2, w3
    result = ' '.join(gen_words)
    return result


def sign_period(ast_sign):
    periods = {'Овен': '20 марта — 19 апреля','Телец': '20 апреля — 20 мая', 'Близнецы':
'21 мая — 20 июня','Рак':
'21 июня — 22 июля', 'Лев':
'23 июля — 22 августа', 'Дева':
'23 августа — 22 сентября', 'Весы':
'23 сентября — 22 октября', 'Скорпион':
'23 октября — 21 ноября', 'Стрелец':
'22 ноября — 21 декабря', 'Козерог':
'22 декабря — 19 января', 'Водолей':
'21 января — 18 февраля', 'Рыбы':
'19 февраля — 19 марта'}


    get_period = periods[ast_sign]
    return get_period
sign = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева","Весы","Скорпион", "Стрелец", "Козерог", "Водолец", "Рыбы"]

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
        bot.reply_to(message, "Привет! Тебя приветствует известный ученый психолог Форер! Он может предсказать твое будущее! Думаешь компьютеры плохие астрологи? Давай проверим! Хочешь? /Yes")

@bot.message_handler(commands=['No'])
def no_message(message):
    bot.send_message(message.chat.id, "Жаль, жаль! Если передумаешь нажимай /Yes, твой Форер")
@bot.message_handler(commands=['Yes'])
def yes_message(message):
        bot.send_message(message.chat.id, "Здорово, напиши нам свой знак зодиака ")

@bot.message_handler(func=lambda message: True)
def guess_message(message):
    if message.text in sign:
        ast_sign = message.text
        h = getTextFromHoroscope(ast_sign)
        this_period = sign_period(ast_sign)
        bot.send_message(message.chat.id,
                         "Значит так, ты" + " " + ast_sign + "" + "(" + this_period + ")" + "." + " "+ "Вот что говорят о тебе звезды:" + "" + "" + h)


    else:
        if message.text == "Нет" or message.text == "нет" or message.text == "в жопу":
            bot.send_message(message.chat.id,
                         "Что ж ты так грубо то...Да бог с тобой! Лучше попробуй заново /start")
        else:
            if message.text == "спасибо" or message.text == "круто" or message.text == "класс":
                bot.send_message(message.chat.id,
                                 "Я рад, что тебе понравилось, заходи еще завтра, тебя будет ждать свеженький гороскоп:)")
            else:
                bot.send_message(message.chat.id,
                         "Астролог Форер к вашим услугам, чтобы начать нажми /start")


bot.polling()
