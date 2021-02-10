import os
import json
import requests
from numpy import argmax
from pandas import read_csv
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import text, sequence
from logger import get_commands_logger

MAX_LEN = 8
PATH = os.getcwd()
comm_logger = get_commands_logger('commands_logger')

def get_tokenizer():
    with open(PATH + '/config/ruvec/vocab.txt') as f:
        words = [i[:-1] for i in f.readlines()]
    csv = read_csv(PATH + '/assets/csv/names.csv')
    train = csv['text']
    token = text.Tokenizer(num_words=None)
    token.fit_on_texts(list(train) + words)
    return token

tokenizer = get_tokenizer()


def open_browser(*args):
    os.system('xdg-open http:// 2>>logs/functions_errors.log')
    comm_logger.info("Browser opened")
    return (2, 'Открываю браузер')

def open_explorer(*args):
    os.system('xdg-open . 2>>logs/functions_errors.log')
    comm_logger.info("Explorer opened")
    return (0,'Проводник')

def shutdown(*args):
    os.system('shutdown -h now 2>>logs/functions_errors.log')
    comm_logger.info("Shutdowning")
    return (1,'Выключение')

def symbol(*args):
    return (3,'mnogo')

def weather():
    ip = requests.get('https://ip.beget.ru').text[:-1]
    send_url = f'http://ipinfo.io/{ip}/geo?token=3edfdea826f009'
    r = requests.get(send_url).json()
    city = r['city'].replace(' ','%20')
    api_key = json.load(open(PATH+'/config/settings.json'))['owm_api_key']
    return (4,requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},ru&appid={api_key}').text)

def open_terminal():
    if os.environ['XDG_CURRENT_DESKTOP'] == 'GNOME':
        os.system('gnome-terminal')
        return (5,'term opened')
    else:
        return (5, 'idk your de')

def new_name(*args):
    txt = args[0]
    model = load_model(PATH + '/assets/models/name_predictor/')
    seq_text = tokenizer.texts_to_sequences([txt])
    padded_text = sequence.pad_sequences(seq_text, maxlen=MAX_LEN)
    predict = model.predict(padded_text)[0]
    txt = [0] * (7-len(txt.split())) + txt.split()
    if max(predict) > 0.4:
        comm_logger.info("Recognized name is " + txt[argmax(predict)-1])
        return (6,txt[argmax(predict)-1])
    else:
        return (6, 'try again')


Labels2Commands = {0: open_explorer, 1: shutdown, 2: open_browser, 3: symbol, 4: weather, 5: open_terminal, 6: new_name}