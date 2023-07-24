import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Sample user preferences and input text
user_preferences = ['sports', 'technology', 'music']
input_text = "I'm feeling excited about the latest technology developments."

# API endpoint for news articles
news_api_url = "https://newsapi.org/v2/top-headlines"

# API key for accessing news articles (replace with your own)
api_key = ""

# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Preprocess user preferences and input text
processed_preferences = ' '.join(user_preferences)
processed_text = input_text.lower()

# Generate feature vectors for user preferences and input text
corpus = [processed_preferences] + [processed_text]
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(corpus)
user_preference_vector = feature_vectors[0]
input_text_vector = feature_vectors[1]

# Calculate cosine similarity between user preferences and input text
similarity_score = cosine_similarity(user_preference_vector, input_text_vector)[0][0]

# Perform sentiment analysis on input text
sentiment_score = sia.polarity_scores(input_text)['compound']

# Fetch news articles from the API
filtered_articles = []
categories = ['sports', 'technology', 'music']  # Categories to search in

for category in categories:
    params = {
        'apiKey': api_key,
        'language': 'en',
        'pageSize': 10,
        'category': category,
        'q': ''
    }
    try:
        response = requests.get(news_api_url, params=params)
        response.raise_for_status()
        articles = response.json()['articles']
        # print(articles)

        for article in articles:
            title = article['title']
            content = article['description']
            if content is not None:
                processed_content = content.lower()
                article_vector = vectorizer.transform([processed_content])
                article_similarity = cosine_similarity(user_preference_vector, article_vector)[0][0]
                article_sentiment = sia.polarity_scores(content)['compound']

                if article_similarity > 0.5 and article_sentiment > 0.1:
                    filtered_articles.append((title, content))

        if filtered_articles:
            break  # Stop searching categories once we find at least one recommendation

    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching news articles:", e)

# If no articles matched the criteria, include one with the highest similarity
if not filtered_articles:
    highest_similarity_article = max(
        (a for a in articles if a['description'] is not None),
        key=lambda x: cosine_similarity(user_preference_vector, vectorizer.transform([x['description'].lower()]))[0][0]
    )
    title = highest_similarity_article['title']
    content = highest_similarity_article['description']
    filtered_articles.append((title, content))

# Print personalized recommendations
print("Personalized Recommendations:")
print("Similarity score:", similarity_score)
print("Sentiment score:", sentiment_score)
print("Recommended articles:")
for article in filtered_articles:
    print("- Title:", article[0])
    print("  Content:", article[1])
    print()
