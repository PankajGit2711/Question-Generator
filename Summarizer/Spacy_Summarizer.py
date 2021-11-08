import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from bs4 import BeautifulSoup
import urllib.request

def text_summarizer(raw_text):
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    word_frequencies = {}

    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_freq = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_freq)
    sentence_list = [sentence for sentence in docx.sents]

    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 50:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentence = nlargest(5, sentence_scores, key=sentence_scores.get)
    final_sentence = [w.text for w in summarized_sentence]
    summary = ' '.join(final_sentence)
    return summary

data = input()
read_data = urllib.request.urlopen("https://en.wikipedia.org/wiki/" + data).read()
soup = BeautifulSoup(read_data, 'lxml')
text = " "
for paragraph in soup.find_all('p'):
     text += paragraph.text

x = text_summarizer(raw_text=text)
print(x)
