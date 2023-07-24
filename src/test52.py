import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load the CSV file
data = pd.read_csv('labeled_dataset.csv')

# Extract the text and corresponding labels
texts = data['text'].values
labels = data['topic'].values

# Text preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # Tokenize the text
    words = text.split()

    # Remove stop words and lemmatize the words
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

    # Rejoin the words into a single string
    return ' '.join(words)

# Preprocess the text data
texts = [preprocess(text) for text in texts]

# Convert the text into numerical features using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train a logistic regression classifier
classifier = LogisticRegression()
classifier.fit(X, labels)

# Example text to predict the topic
new_text = ['This is the best wood']

# Preprocess the new text
new_text = [preprocess(text) for text in new_text]

# Convert the new text into numerical features
new_text_features = vectorizer.transform(new_text)

# Predict the topic of the new text
predicted_topic = classifier.predict(new_text_features)

print('Predicted topic:', predicted_topic[0])
