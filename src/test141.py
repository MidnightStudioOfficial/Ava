import nltk
from nltk.corpus import wordnet
#from PyDictionary import PyDictionary
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import sys, re
import requests
from bs4 import BeautifulSoup

def _get_soup_object(url, parser="html.parser"):
    return BeautifulSoup(requests.get(url).text, parser)

class PyDictionary(object):

    def __init__(self, *args):
        try:
            if isinstance(args[0], list):
                self.args = args[0]
            else:
                self.args = args
        except:
            self.args = args

    
    def printMeanings(self):
        dic = self.getMeanings()
        for key in dic.keys():
            print(key.capitalize() + ':')
            for k in dic[key].keys():
                print(k + ':')
                for m in dic[key][k]:
                    print(m)

    def printAntonyms(self):
        antonyms = dict(zip(self.args,self.getAntonyms(False)))
        for word in antonyms:
            print(word+':')
            print(', '.join(antonyms[word]))

    def printSynonyms(self):
        synonyms = dict(zip(self.args,self.getSynonyms(False)))
        for word in synonyms:
            print(word+':')
            print(', '.join(synonyms[word]))

    def getMeanings(self):
        out = {}
        for term in self.args:
            out[term] = self.meaning(term)
        return out

    def getSynonyms(self, formatted=True):
        return [self.synonym(term, formatted) for term in self.args]

    def __repr__(self):
        return "<PyDictionary Object with {0} words>".format(len(self.args))

    def __getitem__(self, index):
        return self.args[index]

    def __eq__(self):
        return self.args

    def getAntonyms(self, formatted=True):
        return [self.antonym(term, formatted) for term in self.args]

    @staticmethod
    def synonym(term, formatted=False):
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
                section = data.find('div', {'class': 'type-synonym'})
                spans = section.findAll('a')
                synonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: synonyms}
                return synonyms
            except:
                print("{0} has no Synonyms in the API".format(term))


    @staticmethod
    def antonym(term, formatted=False):
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
                section = data.find('div', {'class': 'type-antonym'})
                spans = section.findAll('a')
                antonyms = [span.text.strip() for span in spans]
                if formatted:
                    return {term: antonyms}
                return antonyms
            except:
                print("{0} has no Antonyms in the API".format(term))

    @staticmethod
    def meaning(term, disable_errors=False):
        if len(term.split()) > 1:
            print("Error: A Term must be only a single word")
        else:
            try:
                html = _get_soup_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
                    term))
                types = html.findAll("h3")
                length = len(types)
                lists = html.findAll("ul")
                out = {}
                for a in types:
                    reg = str(lists[types.index(a)])
                    meanings = []
                    for x in re.findall(r'\((.*?)\)', reg):
                        if 'often followed by' in x:
                            pass
                        elif len(x) > 5 or ' ' in str(x):
                            meanings.append(x)
                    name = a.text
                    out[name] = meanings
                return out
            except Exception as e:
                if disable_errors == False:
                    print("Error: The Following Error occured: %s" % e)

def rewrite_sentence(sentence):
    # Create a PyDictionary instance
    dictionary = PyDictionary()
    # Tokenize the sentence
    tokens = nltk.word_tokenize(sentence)
    # Get the part of speech tags for each token
    pos_tags = nltk.pos_tag(tokens)
    # Rewrite the sentence by replacing nouns with their synonyms
    rewritten_tokens = []
    for token, pos in pos_tags:
        if pos.startswith('NN'):
            # Get the synonyms for the noun
            synonyms = dictionary.synonym(token)
            if synonyms:
                # Choose the first synonym
                synonym = synonyms[0]
                rewritten_tokens.append(synonym)
            else:
                rewritten_tokens.append(token)
        else:
            rewritten_tokens.append(token)
    # Join the rewritten tokens to form the new sentence
    rewritten_sentence = ' '.join(rewritten_tokens)
    return rewritten_sentence

def is_worth_the_change(original_sentence, rewritten_sentence):
    # Create a TfidfVectorizer to represent the sentences as vectors
    vectorizer = TfidfVectorizer()
    # Fit the vectorizer on both sentences
    X = vectorizer.fit_transform([original_sentence, rewritten_sentence])
    # Compute the cosine similarity between the two vectors
    similarity = cosine_similarity(X[0], X[1])[0][0]
    # If the similarity is above a certain threshold, consider it worth the change
    return similarity > 0.5

# Example usage
original_sentence = "The cat sat on the mat"
rewritten_sentence = rewrite_sentence(original_sentence)
print(f"Original sentence: {original_sentence}")
print(f"Rewritten sentence: {rewritten_sentence}")
print(f"Worth the change: {is_worth_the_change(original_sentence, rewritten_sentence)}")
