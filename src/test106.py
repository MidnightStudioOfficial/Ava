import nltk
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding

# Load the dataset of user input and bot responses
data = [
    "Hello, how are you?",
    "I'm doing well, thank you. How about you?",
    "I'm doing pretty good too. What have you been up to lately?",
    "Not much, just working and spending time with family. How about you?",
    "Same here. Just trying to stay busy and productive."
]


# Preprocess the data
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
#data = [tokenizer.tokenize(sentence) for sentence in data]
# Join the tokens into sentences
data = [' '.join(sentence) for sentence in data]

# Create n-grams
n = 3
ngrams = [' '.join(ngram) for ngram in ngrams(data, n)]



# Vectorize the n-grams
vectorizer = CountVectorizer(analyzer=lambda x: x)
X = vectorizer.fit_transform(ngrams)

# Split the data into input and output
# Split the data into input and output
X, y = X[:, :-1], X[:, -1]

# Convert the input data to a dense matrix
X = X.toarray()


# Create the model
model = Sequential()
model.add(Embedding(input_dim=len(vectorizer.vocabulary_), output_dim=128))
model.add(LSTM(128))
model.add(Dense(len(vectorizer.vocabulary_), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model
model.fit(X, y, epochs=10)

# Generate a new sentence
sentence = "hwho are you"
for _ in range(10): # generate 10 words
    x = vectorizer.transform(sentence[-n+1:])
    word_index = model.predict(x).argmax()
    word = vectorizer.inverse_transform(word_index)
    sentence.append(word)

print(' '.join(sentence))
