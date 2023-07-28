# import the libraries
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize

# Download the WordNet lemmatizer data and POS tagging data
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

web_sample = [
    "can you search the web for cats",
    "search google for books",
    "google search for hats",
    "who is the president of the united states",
    "what is the capital of the united states",
    "what is the capital of the united states of america",
]
chatbot_sample = [
    "what is the weather like today",
    "I am bored",
    "what is your name",
    "what is your age",
    "what is your gender",
    "what is your favorite color",
]

# Create a WordNet lemmatizer object
lemmatizer = WordNetLemmatizer()

def get_question_pos(text):
    """
    This function takes an input text and returns a list of POS tags for the words in the text.
    """
    tokens = word_tokenize(text.lower())
    pos_tags = pos_tag(tokens)
    return pos_tags

def process(text):
    """
    This function uses sklearn to train a model from each web_sample and chatbot_sample
    to detect if the text is asking to search the web or ask the chatbot a question using TfidfVectorizer, MultinomialNB, and cosine_similarity.
    It also applies Lemmatization and POS tagging to the input text before vectorizing.
    """
    # Lemmatize the input text
    lemmatized_text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())

    # Get POS tags for the lemmatized text
    pos_tags = get_question_pos(lemmatized_text)

    # Check if the first word is an interrogative pronoun (e.g., "what," "who," "where," etc.)
    is_question = pos_tags[0][1] in ['WP', 'WP$', 'WRB']

    # Create an advanced TfidfVectorizer object
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)

    # Fit the advanced vectorizer on the web_sample and chatbot_sample data
    vectorizer.fit(web_sample + chatbot_sample)

    # Transform the lemmatized text into a TF-IDF vector
    text_vector = vectorizer.transform([lemmatized_text])

    # Create a MultinomialNB classifier object
    classifier = MultinomialNB()

    # Fit the classifier on the web_sample and chatbot_sample data
    classifier.fit(vectorizer.transform(web_sample + chatbot_sample), ['web'] * len(web_sample) + ['chatbot'] * len(chatbot_sample))

    # Calculate the cosine similarity between the text vector and the web_sample and chatbot_sample vectors
    similarity_web = cosine_similarity(text_vector, vectorizer.transform(web_sample))
    similarity_chatbot = cosine_similarity(text_vector, vectorizer.transform(chatbot_sample))

    # If the question starts with an interrogative pronoun, classify as chatbot
    if is_question:
        return 'chatbot'
    # Otherwise, return the class label with the highest cosine similarity
    elif similarity_web.any() > similarity_chatbot.any():
        return 'web'
    else:
        return 'chatbot'

while True:
    text = input("Enter a question: ")
    if text.lower() == 'exit':
        break
    print(process(text))
    print()
