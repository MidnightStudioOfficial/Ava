from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


# Sample data for intent classification (You can expand this with more examples)
data = [
    ("What is a cat?", "WEB_SEARCH"),
    ("What is your favorite color?", "CHATBOT_RESPONSE"),
    ("What is your name?", "CHATBOT_RESPONSE"),
    ("who is ava max?", "WEB_SEARCH"),
    # Add more labeled examples here
]

# Separate the training data into features and labels
train_texts, train_labels = zip(*data)

# Feature extraction using TfidfVectorizer
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

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
