from flask import Flask, render_template, url_for, request
import wikipedia
import nltk
import requests
import nltk.data
from bs4 import BeautifulSoup
import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    r = requests.get('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8081/api/all')
    data = r.json()
    for i in data:
        final_data = i['command']

    # if len(sys.argv) == 1:
    #     print (sys.argv[0])
    #     print("Please enter topic in command line:")
    #     print("python Questionizer.py [topic]")
    wikiString = final_data

    print("")

    topic = (wikipedia.page(wikiString))
    print("Topic: " + topic.title)
    # sentenceTokenizedText = nltk.sent_tokenize(topic.summary)
    summary = topic.summary
    print("Summary Paragraph:")
    # print(type(summary))
    print("")

    post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8082/api/summary?'+'summary='+summary)
    posted_r = post_r.json()

    # wordTokenizedSentence = nltk.word_tokenize(sentenceTokenizedText[0])
    # print("Sentence to be converted (tokenized):")
    # print(wordTokenizedSentence)
    # print("")

    # posTaggedWords = nltk.pos_tag(wordTokenizedSentence)
    # print("POS Tagged Sentence:")
    # print(posTaggedWords)
    # print("")

    # namedEntities = nltk.ne_chunk(posTaggedWords)
    # print("Sentence with entity recognition:")
    # print(namedEntities)
    # print("")
    return summary


if __name__ == '__main__':
	app.run(debug=True)
