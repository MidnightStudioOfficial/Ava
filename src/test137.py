from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def is_user_referring_to_chatbot(input_text):
    # Define pronouns that can refer to the user
    user_pronouns = ['I', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves']

    # Tokenize the input text
    words = word_tokenize(input_text)

    # Check if any pronouns are present and if they refer to the user
    for word in words:
        if word.lower() in user_pronouns:
            return False  # User is referring to themselves

    return True  # User is referring to the chatbot

# Sample labeled data for training the classifier
labeled_data = [
    ("I need your help", "user"),
    ("What can you do for me?", "user"),
    ("How are you?", "chatbot"),
    ("Tell me a joke", "user"),
    ("You are very helpful", "chatbot"),
    ("I am feeling happy", "user"),
    ("Can you provide some information?", "user"),
    ("You are doing a great job!", "chatbot"),
]

# Separate the input (X) and labels (y)
X, y = zip(*labeled_data)

# Convert the input text to TF-IDF features
tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenize, lowercase=True)
X_tfidf = tfidf_vectorizer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Train the classifier (Multinomial Naive Bayes in this case)
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = classifier.predict(X_test)

# Calculate accuracy on the test set
accuracy = accuracy_score(y_test, y_pred)
print("Classifier accuracy:", accuracy)

# Test the classifier with new user inputs
while True:
    user_input = input("You: ")
    user_input_tfidf = tfidf_vectorizer.transform([user_input])
    prediction = classifier.predict(user_input_tfidf)[0]
    
    if prediction == "user":
        print("User is referring to themselves.")
    else:
        print("User is referring to the chatbot.")
