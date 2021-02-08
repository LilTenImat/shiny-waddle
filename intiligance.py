import os
import pyaudio
import wave
import requests
import json
import speech_recognition as speech_recog
from nltk.stem.snowball import RussianStemmer
from pickle import load
from sklearn.preprocessing import normalize
from logger import get_commands_logger, get_ml_logger
from bs4 import BeautifulSoup

PATH = os.getcwd()

mic = speech_recog.Microphone()
recog = speech_recog.Recognizer()
stemmer = RussianStemmer(False)
solver = load(open(r'config/RFC.sav','rb'))

comm_logger = get_commands_logger('commands_logger')
ml_logger = get_ml_logger('ml_logger')
def open_browser():
    os.system('xdg-open http:// 2>>logs/functions_errors.log')
    comm_logger.info("Browser opened")
    return (2, 'Открываю браузер')

def open_explorer():
    os.system('xdg-open . 2>>logs/functions_errors.log')
    comm_logger.info("Explorer opened")
    return (0,'Проводник')

def shutdown():
    os.system('shutdown -h now 2>>logs/functions_errors.log')
    comm_logger.info("Shutdowning")
    return (1,'Выключение')

def symbol():
    return (3,'mnogo')

def weather():
    ip = requests.get('https://ip.beget.ru').text[:-1]
    send_url = f'http://ipinfo.io/{ip}/geo?token=3edfdea826f009'
    r = requests.get(send_url).json()
    city = r['city'].replace(' ','%20')
    api_key = json.load(open(PATH+'/config/settings.json'))['owm_api_key']
    return (4,requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},ru&appid={api_key}').text)

def open_terminal():
    os.system('gnome-terminal')
    return (5,'term opened')

Labels2Commands = {0: open_explorer, 1: shutdown, 2: open_browser, 3: symbol, 4: weather, 5: open_terminal}

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
                print(probabilities)
                if probabilities[0][command] > 0.5:
                    return Labels2Commands[command]()
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
