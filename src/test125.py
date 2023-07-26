from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from collections import defaultdict

# Sample data for intent classification (You can expand this with more examples)
data = [
    ("What is a cat?", "WEB_SEARCH"),
    ("What is your favorite color?", "CHATBOT_RESPONSE"),
    ("What is your name?", "CHATBOT_RESPONSE"),
    ("who is ava max?", "WEB_SEARCH"),
    # Add more labeled examples here
]

# Function to extract co-occurrence patterns from the training data
def extract_co_occurrence_patterns(data):
    word_pairs_count = defaultdict(int)
    for text, label in data:
        words = text.lower().split()
        for i in range(len(words) - 1):
            word_pair = (words[i], words[i + 1])
            word_pairs_count[word_pair] += 1
    return word_pairs_count

# Separate the training data into features and labels
train_texts, train_labels = zip(*data)

# Feature extraction using TfidfVectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# Extract co-occurrence patterns and their counts
word_pairs_count = extract_co_occurrence_patterns(data)

# Function to convert co-occurrence patterns to features for a given query
def extract_co_occurrence_features(query):
    query = query.lower()
    words = query.split()
    features = []
    for i in range(len(words) - 1):
        word_pair = (words[i], words[i + 1])
        features.append(word_pairs_count[word_pair])
    return features

# Train the LinearSVC classifier
classifier = LinearSVC()
classifier.fit(X_train, train_labels)

# Function for web search using Google search
def perform_web_search(query):
    return "No relevant results found."

# Function for the chatbot's response
def get_chatbot_response(query):
    intent = classifier.predict(vectorizer.transform([query]))[0]
    if intent == "WEB_SEARCH":
        return perform_web_search(query)
    else:
        # Extract co-occurrence patterns as features
        co_occurrence_features = extract_co_occurrence_features(query)
        # You can use the co_occurrence_features in combination with the TfidfVectorizer output
        # and any other features you might have added to make the final prediction.
        # Replace this with your actual chatbot response generation logic
        return "Chatbot: I'm sorry, I can't answer that question right now."

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Assistant: Goodbye!")
        break
    response = get_chatbot_response(user_input)
    print("Assistant:", response)
