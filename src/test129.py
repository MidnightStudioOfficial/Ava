"""
this code uses sklearn to train a model
to detect if the text is asking to search the web or ask the chatbot a questen
"""
# import the libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

web_sample = [
    "can you search the web for cats",
]
chatbot_sample = [
    "what is the weather like today",
]

def prcess(text):
    """
    this function uses sklearn to train a model from web_sample and chatbot_sample
    to detect if the text is asking to search the web or ask the chatbot a questen
    """
    # create a vectorizer
    vectorizer = TfidfVectorizer()
    # fit the vectorizer
    vectorizer.fit(web_sample)
    # transform the text
    vector = vectorizer.transform([text])
    # calculate the cosine similarity
    cosine_similarity(vector, vectorizer.transform(web_sample))
    cosine_similarity(vector, vectorizer.transform(chatbot_sample))
    # return the result
    if cosine_similarity(vector, vectorizer.transform(web_sample)) > cosine_similarity(vector, vectorizer.transform(chatbot_sample)):
        return "web"
    else:
        return "chatbot"

print(prcess("can you search the web for bats"))