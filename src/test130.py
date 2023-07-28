"""
this code uses sklearn to train a model
to detect if the text is asking to search the web or ask the chatbot a questen
"""
# import the libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB


web_sample = [
    "can you search the web for cats",
    "search google for books",
    "google search for hats",
    "who is the president of the united states",
    "what is the capital of the united states",
]
chatbot_sample = [
    "what is the weather like today",
    "I am board",
    "what is your name",
    "what is your age",
    "what is your gender",
]

def prcess(text):
    """
    this function uses sklearn to train a model from eatch web_sample and chatbot_sample
    to detect if the text is asking to search the web or ask the chatbot a question using TfidfVectorizer, MultinomialNB and cosine_similarity
    """
    # Create a avacned TfidfVectorizer object
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)

    # Fit the avacned vectorizer on the web_sample and chatbot_sample data
    vectorizer.fit(web_sample + chatbot_sample)

    # Transform the text into a TF-IDF vector
    text_vector = vectorizer.transform([text])

    # Create a MultinomialNB classifier object
    classifier = MultinomialNB()

    # Fit the classifier on the web_sample and chatbot_sample data
    classifier.fit(vectorizer.transform(web_sample), web_sample)

    # Calculate the cosine similarity between the text vector and the web_sample and chatbot_sample vectors
    similarity_web = cosine_similarity(text_vector, vectorizer.transform(web_sample))
    similarity_chatbot = cosine_similarity(text_vector, vectorizer.transform(chatbot_sample))

    # Return the class label with the highest cosine similarity
    if similarity_web.any() > similarity_chatbot.any():
        return 'web'
    else:
        return 'chatbot'

while True:
    text = input("Enter a question: ")
    print(prcess(text))
    print()
    if text == 'exit':
        break