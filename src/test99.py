import nltk
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample data for learning user preferences
input_texts = [
    ("I love reading books and playing sports.", "books_sports"),
    ("Music is my passion, especially rock and roll.", "music_rock"),
    ("I enjoy watching movies and going for long walks.", "movies_walks"),
    ("Cooking and trying new recipes is my hobby.", "cooking_recipes"),
    ("I like traveling and exploring new places.", "travel_exploring"),
]

# Initialize NLTK stopwords
nltk.download("stopwords")
stopwords = nltk.corpus.stopwords.words("english")

# Extract features from input text using bag-of-words approach
vectorizer = CountVectorizer(stop_words=stopwords)
corpus = [text for text, _ in input_texts]
X = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()

# Create target labels for training
y = [label for _, label in input_texts]

# Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X, y)

# User feedback loop
user_ratings = {}

while True:
    user_input = input("Please enter your interests and mood (or 'q' to quit): ")
    if user_input.lower() == "q":
        break

    # Extract features from user input using the same vectorizer
    user_input_features = vectorizer.transform([user_input])

    # Predict user preferences using the trained classifier
    predicted_label = classifier.predict(user_input_features)[0]

    # Generate personalized recommendations based on predicted label
    recommendations = []
    if predicted_label == "books_sports":
        recommendations = ["Read a new book", "Go for a run"]
    elif predicted_label == "music_rock":
        recommendations = ["Listen to some rock music", "Attend a live concert"]
    elif predicted_label == "movies_walks":
        recommendations = ["Watch a movie", "Take a long walk in a park"]
    elif predicted_label == "cooking_recipes":
        recommendations = ["Try a new recipe", "Cook a meal for friends"]
    elif predicted_label == "travel_exploring":
        recommendations = ["Plan a weekend trip", "Explore a new city"]

    # Print personalized recommendations
    print("Based on your interests and mood, I recommend the following:")
    for recommendation in recommendations:
        print("- " + recommendation)

    # Prompt for user feedback
    rating = input("Please rate the recommendations (1-5, 5 being the highest): ")
    user_ratings[user_input] = int(rating)

    # Retrain the classifier with updated ratings
    ratings_corpus = []
    ratings_labels = []
    for rating_text, rating_label in user_ratings.items():
        ratings_corpus.append(rating_text)
        ratings_labels.append(rating_label)

    X_ratings = vectorizer.transform(ratings_corpus)
    y_ratings = ratings_labels
    classifier.fit(X_ratings, y_ratings)
