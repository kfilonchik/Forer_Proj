import json
from random import choice
import random
from datetime import date
import datetime

horoscope = {}
signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева","Весы","Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]

def get_text_from_horoscope(sign):

    d = date.today()
    if sign not in signs:
        return TypeError;

    if (d, sign) not in horoscope:
        horoscope[(d, sign)] = gen_horoscope()


    data = {}
    data['sign'] = sign
    data['date'] = (d.day, d.year)
    data['text'] = horoscope[(d, sign)]

    json_data = json.dumps(data)

    return json_data

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


print(get_text_from_horoscope("Лев"))
