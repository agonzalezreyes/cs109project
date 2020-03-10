import numpy as np
import re
import clean
import pandas as pd
from collections import Counter

stop_words = clean.stop_words

def BOW(sentences):
    vocab = tok(sentences)
    print("word list for doc : " + vocab)
    for sentence in sentences:
        words = get_words(sentence)
        bag_vector = np.zeros(len(vocab))
        for w in words:
            for i,word in enumerate(vocab):
                if word == w:
                    bag_vector[i] += 1
        print(sentence + str(np.array(bag_vector)))

def get_words(sentence):
    words = sentence.split(" ")
    cleaned = [w for w in words if w not in stop_words]
    return cleaned

def tok(sentences):
    words = []
    for sen in sentences:
        w = get_words(sen)
        words.extend(w)
    words = sorted(words)
    return words

def freq_df(tweets, num=20):
    freq = Counter(tok(tweets)).most_common(num)
    freq_df = pd.DataFrame(freq, columns=['word', 'freq'])
    return freq_df
