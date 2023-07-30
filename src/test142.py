import nltk
from nltk.corpus import wordnet
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO
dictionary = MultiDictionary()

#dictionary = SpellChecker()


def getWordSuggestions(word):
    candidates = [dictionary.synonym('en', str(word))]
    return candidates

def rewrite_sentence(sentence):
    tokens = nltk.word_tokenize(sentence)
    for i in tokens:
        print(getWordSuggestions(i))

original_sentence = "The cat sat on the mat"
rewritten_sentence = rewrite_sentence(original_sentence)
