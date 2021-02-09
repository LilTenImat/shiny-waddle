import os
import pyaudio
import wave
import requests
import json
import speech_recognition as speech_recog
from pandas import read_csv
from numpy import argmax
from nltk.stem.snowball import RussianStemmer
from pickle import load
from sklearn.preprocessing import normalize
from tensorflow.keras.preprocessing import sequence, text
from tensorflow.keras.models import  load_model
from logger import get_commands_logger, get_ml_logger

PATH = os.getcwd()
MAX_LEN = 8
def get_tokenizer():
    csv = read_csv(PATH + '/assets/csv/names.csv')
    train = csv['text']
    token = text.Tokenizer(num_words=None, oov_token='холодильник')
    token.fit_on_texts(list(train))
    return token

tokenizer = get_tokenizer()
mic = speech_recog.Microphone()
recog = speech_recog.Recognizer()
stemmer = RussianStemmer(False)
solver = load(open(PATH + r'/assets/models/RFC.sav','rb'))

comm_logger = get_commands_logger('commands_logger')
ml_logger = get_ml_logger('ml_logger')
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
    print('deb')
    model = load_model(PATH + '/assets/models/name_predictor/')
    seq_text = tokenizer.texts_to_sequences([txt])
    padded_text = sequence.pad_sequences(seq_text)
    predict = model.predict(padded_text)[0]
    print(predict)
    if max(predict) > 0.4:
        print(argmax(predict))
        return (6,txt[argmax(predict)])
    else:
        return (6, 'try again')


Labels2Commands = {0: open_explorer, 1: shutdown, 2: open_browser, 3: symbol, 4: weather, 5: open_terminal, 6: new_name}

class Worker():
    def __init__(self):
        pass
    
    @staticmethod
    def on_command(text=None):
        if text:
            try:
                print('Stemming...')
                stemmed_text = stemmer.stem(text)
                print(stemmed_text)
                command = solver.predict([stemmed_text])[0]
                probabilities = solver.predict_proba([stemmed_text])
                print(probabilities, command)
                if probabilities[0][command] > 0.5:
                    return Labels2Commands[command](text)
                else:
                    return (-1, text)
            except Exception as e:
                print("Error: " + str(e))
                return (-2, e)
        with mic as audio_file:
            print("Speak Please")

            recog.adjust_for_ambient_noise(audio_file)
            audio = recog.listen(audio_file)

            print("Converting Speech to Text...")

            try:
                text = recog.recognize_google(audio, language='ru-RU')
                print('Stemming...')
                stemmed_text = stemmer.stem(text)
                print(stemmed_text)
                command = solver.predict([stemmed_text])[0]
                probabilities = solver.predict_proba([stemmed_text])
                print(probabilities)
                if probabilities[0][command] > 0.5:
                    return Labels2Commands[command]()
                else:
                    return (-1, text)
            except Exception as e:
                print("Error: " + str(e))
                return (-2, e)
