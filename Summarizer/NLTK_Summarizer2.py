from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import numpy as np
import heapq
import nltk
from nltk.corpus import stopwords

def summarizer(raw_text):
    source = urllib.request.urlopen('https://en.wikipedia.org/wiki/'+ raw_text).read()
    soup = BeautifulSoup(source, 'lxml')
    # para = soup.find_all('p')
    text = " "
    for paragraph in soup.find_all('p'):
        text += paragraph.text

    text = re.sub(r'\[[0-9]\]*',' ',text)
    text = re.sub(r'[0-9]+\]',' ',text)
    text = re.sub(r'\s+',' ',text)
    cleantext = text.lower()
    cleantext = re.sub(r'\W',' ',cleantext)
    cleantext = re.sub(r'[0-9]+',' ',cleantext)
    cleantext = re.sub(r'\s+',' ',cleantext)
    cleantext = re.sub(r'\s+[a-z]\s+',' ',cleantext)

    sentences = nltk.sent_tokenize(text)
    stop_words = set(stopwords.words('english'))

    word2count = {}
    for word in nltk.word_tokenize(cleantext):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    word_freq = heapq.nlargest(len(word2count), word2count, key=word2count.get)

    for key in word2count.keys():
        word2count[key] = word2count[key] / max(word2count.values())

    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if (len(sentence.split(' '))) < 70:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]
    best_sentence = heapq.nlargest(5, sent2score, key=sent2score.get)
    for sentence in best_sentence:
        return sentence


text = input()
x = summarizer(text)
print(x)
