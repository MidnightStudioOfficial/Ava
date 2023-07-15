import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample user input text
user_text = [
    "I love action movies and adventure sports.",
    "Feeling bored today, any recommendations?",
    "I enjoy reading fantasy novels and playing video games.",
    "I'm feeling stressed, need something relaxing to do.",
    "I'm in the mood for some good food."
]

# Sample recommendation categories
recommendations = {
    'action': [
        "Watch 'Mission Impossible'.",
        "Go skydiving for an adrenaline rush."
    ],
    'adventure': [
        "Try bungee jumping for an exciting experience.",
        "Watch 'Indiana Jones' movies for a thrilling adventure."
    ],
    'boredom': [
        "Read a mystery novel like 'Sherlock Holmes'.",
        "Explore new hobbies like painting or cooking."
    ],
    'fantasy': [
        "Read 'Harry Potter' series for a magical journey.",
        "Play 'The Witcher' video game for a fantasy adventure."
    ],
    'relaxation': [
        "Listen to calm music and practice meditation.",
        "Take a walk in nature to destress."
    ],
    'food': [
        "Try a new restaurant in town and sample their cuisine.",
        "Cook a delicious meal at home using a new recipe."
    ]
}

# Initialize NLTK's sentiment intensity analyzer
sid = SentimentIntensityAnalyzer()

# Learn user preferences
vectorizer = TfidfVectorizer()
text_vectors = vectorizer.fit_transform(user_text)

# Get user's mood and interests
mood_index = 0
interests_index = 2

# Extract user's mood
mood_text = user_text[mood_index]
mood_sentiment = sid.polarity_scores(mood_text)
mood_category = max(mood_sentiment, key=lambda x: mood_sentiment[x])

# Extract user's interests
interests_text = user_text[interests_index]
interests_tokens = nltk.word_tokenize(interests_text)
interests = [word for word in interests_tokens if word.isalpha()]

# Get recommendations based on mood and interests
recommended = []
if mood_category in recommendations:
    recommended.extend(recommendations[mood_category])
if interests:
    for word in interests:
        if word in recommendations:
            recommended.extend(recommendations[word])

# Print recommendations
if recommended:
    print("Recommended activities:")
    for activity in recommended:
        print("- " + activity)
else:
    print("No personalized recommendations available.")
