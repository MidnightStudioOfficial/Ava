import nltk
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB

# Download the Brown Corpus if not already downloaded
nltk.download("brown")

# Load the Brown Corpus and extract sentences
from nltk.corpus import brown

sentences = brown.sents()

# Flatten the sentences into a single list of words
words = [word for sent in sentences for word in sent]

# Generate n-grams (in this case, we'll use 3-grams, but you can try different values)
n = 3
ngrams = [words[i:i + n] for i in range(len(words) - n + 1)]

# Convert n-grams back to sentences
sentences = [" ".join(ngram) for ngram in ngrams]

# Create the target words (next word in each n-gram)
targets = [ngram[-1] for ngram in ngrams]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(sentences, targets, test_size=0.2, random_state=42)

# Create the n-gram vectorizer and the Naive Bayes model
vectorizer = CountVectorizer(ngram_range=(n - 1, n - 1), lowercase=False)
classifier = MultinomialNB()

# Build the pipeline
pipeline = make_pipeline(vectorizer, classifier)

# Train the model
pipeline.fit(X_train, y_train)

# Function to autocomplete text
def autocomplete(text, max_suggestions=5):
    last_ngram = text.split()[-(n - 1):]
    prefix = " ".join(last_ngram)
    suggestions = pipeline.predict([prefix])[0]
    suggestions = list(set(suggestions))  # Remove duplicate suggestions
    random.shuffle(suggestions)  # Shuffle the suggestions for randomness
    return suggestions[:max_suggestions]

# Main loop for user interaction
while True:
    user_input = input("Enter a text to autocomplete (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    suggestions = autocomplete(user_input)
    print("Autocomplete suggestions:", suggestions)

