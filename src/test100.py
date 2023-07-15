import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

class PersonalizedRecommendations:
    def __init__(self):
        self.user_preferences = []
        self.tfidf_vectorizer = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        self.tfidf_matrix = None

    def tokenize(self, text):
        return nltk.word_tokenize(text.lower())

    def learn_preferences(self, input_text):
        self.user_preferences.append(input_text)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.user_preferences)

    def generate_recommendations(self, input_text):
        self.learn_preferences(input_text)

        similarities = cosine_similarity(self.tfidf_matrix[-1], self.tfidf_matrix[:-1])
        similar_indices = similarities.argsort().flatten()[::-1]

        recommendations = []
        for index in similar_indices:
            recommendations.append(self.user_preferences[index])

        return recommendations

    def suggest_todo_list(self, mood, interests):
        todo_list = []

        # Example suggestions based on mood
        if mood == 'happy':
            todo_list.append('Go for a walk in the park')
            todo_list.append('Watch a comedy movie')
        elif mood == 'sad':
            todo_list.append('Listen to uplifting music')
            todo_list.append('Read a motivational book')

        # Example suggestions based on interests
        if 'sports' in interests:
            todo_list.append('Play a game of soccer')
            todo_list.append('Go for a swim')
        if 'reading' in interests:
            todo_list.append('Visit the local library')
            todo_list.append('Start reading a new book')

        random.shuffle(todo_list)  # Randomize the order of suggestions

        return todo_list


# Example usage
recommendations = PersonalizedRecommendations()

# Learn user preferences from input text
recommendations.learn_preferences("I love watching movies")
recommendations.learn_preferences("I enjoy playing video games")
recommendations.learn_preferences("I like going on outdoor adventures")

# Generate recommendations based on input text
generated_recommendations = recommendations.generate_recommendations("I want to find something fun to do")

print("Generated Recommendations:")
for recommendation in generated_recommendations:
    print(recommendation)

# Suggest todo list based on mood and interests
suggested_todo_list = recommendations.suggest_todo_list('happy', ['sports', 'reading'])

print("\nSuggested Todo List:")
for suggestion in suggested_todo_list:
    print(suggestion)
