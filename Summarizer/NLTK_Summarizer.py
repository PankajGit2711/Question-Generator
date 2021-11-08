import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
from bs4 import BeautifulSoup
import urllib.request
import re
import requests

def nltk_summarizer(scrapped_data):

    # scrapped_data = re.sub(r"\[[0-9]\]*", ' ', text)
    # scrapped_data = re.sub(r"[0-9]+\]", ' ', text)
    # scrapped_data = re.sub(r"\s+", ' ', text)
    # scrapped_data = text.lower()
    # scrapped_data = re.sub(r'\W+', ' ', text)
    # scrapped_data = re.sub(r'[0-9]+',' ', scrapped_data)
    # scrapped_data = re.sub(r'\s+',' ', scrapped_data)
    # scrapped_data = re.sub(r'\s+[a-z]\s+',' ', scrapped_data)

    StopWords = set(stopwords.words("english"))
    word_frequencies = {}

    for word in nltk.word_tokenize(scrapped_data):
        if word not in StopWords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_freq = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_freq)

    sentence_list = nltk.sent_tokenize(scrapped_data)
    sentence_scores = {}

    for sentence in sentence_list:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < 70:
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

r = requests.get('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8081/api/all')
data = r.json()
for i in data:
    final_data = i['command']
    # print(final_data)

read_data = urllib.request.urlopen("https://en.wikipedia.org/wiki/" + final_data).read()
soup = BeautifulSoup(read_data, 'lxml')
text = " "
for paragraph in soup.find_all('p'):
     text += paragraph.text

# payload = '''{'Summary': text}'''
# post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8082/api/summary', json=payload)
# posted_r = post_r.json()
# print(post_r.text)

x = nltk_summarizer(scrapped_data=text)
print(x)

post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8082/api/summary?'+'summary='+x)
posted_r = post_r.json()
print(post_r.text)
