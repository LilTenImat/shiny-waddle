import os
import pyaudio
import wave
import speech_recognition as speech_recog
from nltk.stem.snowball import RussianStemmer
from pickle import load
from sklearn.preprocessing import normalize
from logger import get_logger

mic = speech_recog.Microphone()
recog = speech_recog.Recognizer()
stemmer = RussianStemmer(False)
solver = load(open('finalized_model.sav', 'rb'))
tokinizer = load(open('tokenizer.sav', 'rb'))

func_logger = get_logger('func_logger')
func_logger.error('мне плохо',extra={'func': '23123213'})

def open_browser():
    os.system('xdg-open http:// 2>>logs/functions_errors.log')
    func_logger.info("Browser opened")

def open_explorer():
    os.system('xdg-open . 2>>logs/functions_errors.log')
    func_logger.info("Explorer opened")

def shutdown():
    os.system('shutdown -h now 2>>logs/functions_errors.log')
    func_logger.info("Shutdowning")

Labels2Commands = {0: open_explorer, 1: open_browser, 2: shutdown}

class Worker():
    def __init__(self):
        pass
    def on_command(self):
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
                normalized = normalize(tokinizer.texts_to_matrix(stemmed_text))
                command = solver.predict(normalized)[0]
                Labels2Commands[command]()
            except Exception as e:
                print("Error: " + str(e))
