import os
from pickle import load
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

PATH = os.getcwd()


def get_count_vec():
    with open(PATH + r'/assets/models/cv.sav', 'rb') as f:
        return load(f)


def get_svc():
    with open(PATH + r'/assets/models/svc.sav', 'rb') as f:
        return load(f)


def prepare_texts(texts):
    stemer = SnowballStemmer(language='russian')
    x_tokens = [word_tokenize(i, language='russian')
                for i in [j for j in texts]]
    x_stemed = [[stemer.stem(i) for i in j] for j in x_tokens]
    x_stemed = [' '.join(i) for i in x_stemed]
    cv = get_count_vec()
    x_data = cv.transform(x_stemed)
    return x_data.toarray()

if __name__ == '__main__':
    print(prepare_texts(['текст']))[0]
