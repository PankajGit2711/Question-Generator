import wikipedia
import nltk
import nltk.data
import re
import pprint
import requests
import sys

namedEntityToQuestionWordDictionary = {
    "PERSON" : "Who",
    "NORP" : "What",
    "FAC" : "Where",
    "ORG" : "What",
    "GPE" : "What",
    "LOC" : "Where",
    "PRODUCT" : "What",
    "EVENT" : "When",
    "WORK_OF_ART" : "What",
    "LAW" : "What",
    "LANGUAGE" : "What",
    "DATE" : "When",
    "TIME" : "When",
    "PERCENT" : "How much",
    "MONEY" : "How much",
    "QUANTITY" : "How much",
    "ORDINAL" : "How much",
    "CARDINAL" : "How much",
}

def getQuestionWord(namedEntity):
    return namedEntityToQuestionWordDictionary.get(namedEntity, "What")

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
sentenceTokenizedText = nltk.sent_tokenize(topic.summary)
summary = topic.summary
print("Summary Paragraph:")
# print(type(summary))
print("")

post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8082/api/summary?'+'summary='+summary)
posted_r = post_r.json()
print(post_r.text)

wordTokenizedSentence = nltk.word_tokenize(sentenceTokenizedText[0])
print("Sentence to be converted (tokenized):")
print(wordTokenizedSentence)
print("")

posTaggedWords = nltk.pos_tag(wordTokenizedSentence)
print("POS Tagged Sentence:")
print(posTaggedWords)
print("")

namedEntities = nltk.ne_chunk(posTaggedWords)
print("Sentence with entity recognition:")
print(namedEntities)
print("")

phrasePatterns = """
NP: {<DT>*<RBS|JJ|JJR|JJS|VBG>*<CD|NN|NNS|NNP|NNPS>+<IN>*<DT>*<RBS|JJ|JJR|JJS|VBG>*<CD|NN|NNS|NNP|NNPS>+<POS>*<RBS|JJ|JJR|JJS|VBG>*<CD|NN|NNS|NNP|NNPS>*<RB>*<VBN>*<IN>*<DT>*<CD|NN|NNS|NNP|NNPS>*<IN>*<DT>*<CD|NN|NNS|NNP|NNPS>*<,>*<NN|NNS|NNP|NNPS>*}
    {<DT>*<RBS|JJ|JJR|JJS|VBG>*<CD|NN|NNS|NNP|NNPS>+<POS>*<DT>*<RBS|JJ|JJR|JJS|VBG>*<CD|NN|NNS|NNP|NNPS>*<RB>*<VBN>*<IN>*<DT>*<CD|NN|NNS|NNP|NNPS>*<IN>*<DT>*<CD|NN|NNS|NNP|NNPS>*<,>*<CD|NN|NNS|NNP|NNPS>*}
VP: {<V.*>*<TO>*<V.*>+}
"""
phraseChunker = nltk.RegexpParser(phrasePatterns)

wordTree = phraseChunker.parse(posTaggedWords)
print("POS Tagged and Chunked Sentence as Word Tree:")
print(wordTree)
print("")

isSentenceInAcceptableFormat = True
isLookingForFirstNounPhrase = True
isLookingForFirstVerbPhrase = False
isLookingForNounPhrasesAfterVerb = False

print("Noun and Verb Phrases to be used in questions and answers:")
subjectNoun = ""
verb = ""
objectNouns = []

for subtree in wordTree.subtrees():
    if subtree.label() == 'NP':
        if isLookingForFirstNounPhrase:
            subjectNoun = subtree
            subjectNoun = ' '.join(word for word, tag in subjectNoun.leaves())
            print(subjectNoun)
            isLookingForFirstNounPhrase = False
            isLookingForFirstVerbPhrase = True
        if isLookingForNounPhrasesAfterVerb:
            objectNoun = subtree
            objectNoun = ' '.join(word for word, tag in objectNoun.leaves())
            print(objectNoun)
            objectNouns.append(objectNoun)
    if subtree.label() == 'VP':
        if isLookingForFirstVerbPhrase:
            verb = subtree
            verb = ' '.join(word for word, tag in verb.leaves())
            print(verb)
            isLookingForFirstVerbPhrase = False
            isLookingForNounPhrasesAfterVerb = True
        else:
            isSentenceInAcceptableFormat = False

print("")
print("Sentence Suitability:")
if isSentenceInAcceptableFormat == False:
    print("Sentence may not be suitable for questions.")
    print("")
else:
    print("Sentence appears to fit question creation format.")
    print("")

quizQuestions = []

subtreeLabel = ""
for subtree in namedEntities.subtrees():
    if subtreeLabel == "" or subtreeLabel == "S":
        subtreeLabel = subtree.label()
questionWord =  getQuestionWord(subtreeLabel)
print("entity type for determining question word: " + subtreeLabel)
print("Question Word: " + questionWord)
print("")
print("Generated Questions and Answers:")

for objectNoun in objectNouns:
    quizQuestion = "Question: " + questionWord + ' ' + verb + ' ' + subjectNoun + "? Answer: " + objectNoun
    quizQuestions.append(quizQuestion)


# for objectNoun in objectNouns:
#     quizQuestion = "Question: " + questionWord + ' ' + verb + ' ' + objectNoun + "? Answer: " + subjectNoun
#     quizQuestions.append(quizQuestion)

for quizQuestion in quizQuestions:
    quiz = quizQuestion

    post_r = requests.post('http://ec2-13-234-155-85.ap-south-1.compute.amazonaws.com:8083/api/send?'+'input='+quiz)
    posted_r = post_r.json()
    print(post_r.text)
