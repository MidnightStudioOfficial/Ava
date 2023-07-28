from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Download NLTK resources (stopwords and WordNet)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Load the spaCy language model
nlp = spacy.load('en_core_web_sm')

# Function for data preprocessing
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation and convert to lowercase
    tokens = [token.lower() for token in tokens if token.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # Join the processed tokens back into a string
    processed_text = ' '.join(tokens)
    return processed_text

# Sample data for intent classification (You can expand this with more examples)
data = [
    ("What is a cat?", "WEB_SEARCH"),
    ("What is your favorite color?", "CHATBOT_RESPONSE"),
    ("What is your name?", "CHATBOT_RESPONSE"),
    ("What is your favorite food?", "CHATBOT_RESPONSE"),
    ("search google for books", "WEB_SEARCH"),
    ("what is your gender", "CHATBOT_RESPONSE"),
    ("I am board", "CHATBOT_RESPONSE"),
    # Add more labeled examples here
]


# Separate the training data into features and labels
train_texts, train_labels = zip(*data)

# Feature extraction using CountVectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# Train the Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, train_labels)

def extract_pos_tags(text):
    doc = nlp(text)
    pos_tags = [token.pos_ for token in doc]
    return ' '.join(pos_tags)

# Function to process text and get predictions
def process(text):
    # Extract POS tags from the input text
    pos_tags = extract_pos_tags(text)

    # Combine POS tags with the text and convert to features using the trained vectorizer
    X_text = vectorizer.transform([text + ' ' + pos_tags])

    # Predict the intent using the trained classifier
    prediction = classifier.predict(X_text)[0]
    return prediction


# Sample test data
test_data = [
    ("What's the capital of France?", "WEB_SEARCH"),
    ("Tell me a joke.", "CHATBOT_RESPONSE"),
    # Add more test examples here
]

# Separate the test data into features and labels
test_texts, test_labels = zip(*test_data)

# Convert test data to features using the trained vectorizer
X_test = vectorizer.transform(test_texts)

# Predict the intents for the test data
predictions = classifier.predict(X_test)

# Calculate and print the accuracy
accuracy = accuracy_score(test_labels, predictions)
print("Accuracy: {:.2f}".format(accuracy))


# Function for the chatbot's response (using spacy as an example)
def get_chatbot_response(query):
    # Replace this with your actual chatbot response generation logic
    response = "Chatbot: I'm sorry, I can't answer that question right now."
    return response
while True:
    # Example usage
    user_input = input("You: ")
    # Preprocess user input
    user_input = preprocess_text(user_input)

    # Extract POS tags from the user input
    user_input_pos = extract_pos_tags(user_input)

    # Combine POS tags with the user input and convert to features using the trained vectorizer
    X_user = vectorizer.transform([user_input + ' ' + user_input_pos])

    # Predict the intent using the trained classifier
    intent = classifier.predict(X_user)[0]

    if intent == "WEB_SEARCH":
        print("Assistant: Performing a web search for '{}'".format(user_input))
        # Implement the code to perform a Google search here
    else:
        print(get_chatbot_response(user_input))