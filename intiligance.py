import os
import speech_recognition as speech_recog
from nltk.stem.snowball import RussianStemmer
from pickle import load
from logger import get_ml_logger
from commands import Labels2Commands
from utils import prepare_texts

PATH = os.getcwd()
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

mic = speech_recog.Microphone()
recog = speech_recog.Recognizer()
stemmer = RussianStemmer(False)
solver = load(open(PATH + r'/assets/models/svc.sav', 'rb'))

ml_logger = get_ml_logger('ml_logger')


class Worker():
    def __init__(self):
        pass

    @staticmethod
    def on_command(text=None):
        if text:
            try:
                print(text)
                stemmed_text = prepare_texts([text])
                command = solver.predict(stemmed_text)
                probabilities = solver.predict_proba(stemmed_text)
                print(probabilities, command)
                if probabilities[0][command] < 1:
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
                stemmed_text = prepare_texts([text])
                print(stemmed_text)
                command = solver.predict([stemmed_text])[0]
                probabilities = solver.predict_proba([stemmed_text])
                print(probabilities)
                if probabilities[0][command] < 1:
                    return Labels2Commands[command](text)
                else:
                    return (-1, text)
            except Exception as e:
                print("Error: " + str(e))
                return (-2, e)
