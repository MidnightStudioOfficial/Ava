# import the libraries
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.svm import LinearSVC

# Download the WordNet lemmatizer data and POS tagging data
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

web_sample = [
    "can you search the web for cats",
    "search google for books",
    "google search for hats",
    "who is the president of the united states",
    "what is the capital of the united states",
]
chatbot_sample = [
    "what is the weather like today",
    "I am bored",
    "what is your name",
    "what is your age",
    "what is your gender",
]

# Create a WordNet lemmatizer object
lemmatizer = WordNetLemmatizer()

import string
from nltk.corpus import stopwords

# Function to preprocess the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenize the text
    tokens = word_tokenize(text)

    # Lemmatize the tokens
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in lemmatized_tokens if token not in stop_words]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(filtered_tokens)
    return preprocessed_text
# Preprocess the web_sample and chatbot_sample data
preprocessed_web_sample = [preprocess_text(text) for text in web_sample]
preprocessed_chatbot_sample = [preprocess_text(text) for text in chatbot_sample]

def get_question_pos(text):
    """
    This function takes an input text and returns a list of POS tags for the words in the text.
    """
    tokens = word_tokenize(text.lower())
    pos_tags = pos_tag(tokens)
    return ' '.join(tag for word, tag in pos_tags)

def process(text):
    """
    This function uses sklearn and scipy to train a model from each web_sample and chatbot_sample
    to detect if the text is asking to search the web or ask the chatbot a question using CountVectorizer, TfidfTransformer, MultinomialNB, and cosine similarity.
    It also applies Lemmatization and POS tagging to the input text before vectorizing.
    """
    # Lemmatize the input text
    #lemmatized_text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())
    preprocessed_text = preprocess_text(text)
    print(preprocessed_text)

    # Get POS tags for the lemmatized text
    pos_tags = get_question_pos(preprocessed_text)

    # Check if the first word is an interrogative pronoun (e.g., "what," "who," "where," etc.)
    is_question = pos_tags.startswith(('WP', 'WP$', 'WRB'))

    # Create a CountVectorizer object for POS tags
    pos_vectorizer = CountVectorizer()
    pos_vectorizer.fit([get_question_pos(text) for text in preprocessed_web_sample + preprocessed_chatbot_sample])
    pos_vector = pos_vectorizer.transform([pos_tags])

    # Combine POS tags with the lemmatized text
    combined_text = preprocessed_text + " " + pos_tags

    # Create a CountVectorizer object
    vectorizer = CountVectorizer(stop_words='english', lowercase=True)
    vectorizer.fit(web_sample + chatbot_sample)

    # Transform the combined text into a term frequency (TF) vector
    text_vector = vectorizer.transform([combined_text])

    # Create a TfidfTransformer object
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(text_vector)

    # Transform the TF vector into a TF-IDF vector
    text_tfidf_vector = tfidf_transformer.transform(text_vector)

    # Create a MultinomialNB classifier object
    classifier = MultinomialNB()
    #classifier = LinearSVC()

    # Fit the classifier on the web_sample and chatbot_sample data
    classifier.fit(tfidf_transformer.transform(vectorizer.transform(preprocessed_web_sample + preprocessed_chatbot_sample)), ['web'] * len(preprocessed_web_sample) + ['chatbot'] * len(preprocessed_chatbot_sample))

    # Calculate the cosine similarity between the text vector and the web_sample and chatbot_sample vectors
    similarity_web = cosine_similarity(text_tfidf_vector, tfidf_transformer.transform(vectorizer.transform(web_sample)))
    similarity_chatbot = cosine_similarity(text_tfidf_vector, tfidf_transformer.transform(vectorizer.transform(chatbot_sample)))

    # If the question starts with an interrogative pronoun, classify as chatbot
    if is_question:
        return 'chatbot'
    # Otherwise, return the class label with the highest cosine similarity
    elif similarity_web[0][0] > similarity_chatbot[0][0]:
        return 'web'
    else:
        return 'chatbot'

# Evaluate the model
web_count, chatbot_count = 0, 0
for text in web_sample + chatbot_sample:
    prediction = process(text)
    if "web" in text.lower() and prediction == "web":
        web_count += 1
    elif "chatbot" in text.lower() and prediction == "chatbot":
        chatbot_count += 1

total_samples = len(web_sample) + len(chatbot_sample)
print(f"Web Sample Accuracy: {web_count / len(web_sample) * 100:.2f}%")
print(f"Chatbot Sample Accuracy: {chatbot_count / len(chatbot_sample) * 100:.2f}%")
print(f"Overall Accuracy: {(web_count + chatbot_count) / total_samples * 100:.2f}%")

while True:
    text = input("Enter a question: ")
    if text.lower() == 'exit':
        break
    print(process(text))
    print()
