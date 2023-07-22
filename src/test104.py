import random
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding

# Set random seed for reproducibility
random.seed(42)

# Load NLTK resources
nltk.download('punkt')

# Dataset of user input and bot responses
dataset = [
    ("Hello", "Hi! How can I assist you?"),
    ("What's your name?", "I am a chatbot."),
    ("How are you?", "I'm doing well, thank you."),
    # Add more training examples here
]

# Tokenize the dataset
tokenized_dataset = [(nltk.word_tokenize(prompt.lower()), nltk.word_tokenize(response.lower()))
                     for prompt, response in dataset]

# Build the vocabulary
vocabulary = {word for prompt, response in tokenized_dataset for word in prompt} | \
             {word for prompt, response in tokenized_dataset for word in response}

# Generate input-output pairs
input_sequences = []
output_sequences = []

for prompt, response in tokenized_dataset:
    input_sequences.append([list(vocabulary).index(token) for token in prompt])
    output_sequences.append([list(vocabulary).index(token) for token in response])

# Train a logistic regression model
vectorizer = CountVectorizer(tokenizer=nltk.word_tokenize, lowercase=True)
X = vectorizer.fit_transform([prompt for prompt, _ in dataset])
y = [response for _, response in dataset]

logistic_model = LogisticRegression()
logistic_model.fit(X, y)

# Train a language model using LSTM
max_sequence_length = max(len(seq) for seq in input_sequences)

# Pad sequences to have the same length
input_sequences = tf.keras.preprocessing.sequence.pad_sequences(input_sequences,
                                                                maxlen=max_sequence_length,
                                                                padding='post')
output_sequences = tf.keras.preprocessing.sequence.pad_sequences(output_sequences,
                                                                 maxlen=max_sequence_length,
                                                                 padding='post')
vocab_size = len(vocabulary)
embedding_dim = 50

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_sequence_length))
model.add(LSTM(256, return_sequences=True))
model.add(Dense(vocab_size, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(input_sequences, tf.keras.utils.to_categorical(output_sequences, num_classes=vocab_size), epochs=100)

# Generate a response based on user prompt
def generate_response(prompt):
    prompt = prompt.lower()
    vectorized_prompt = vectorizer.transform([prompt])
    predicted_response = logistic_model.predict(vectorized_prompt)

    generated_words = prompt.split()
    while True:
        input_sequence = np.array([list(vocabulary).index(word) for word in generated_words])
        input_sequence = tf.keras.preprocessing.sequence.pad_sequences([input_sequence],
                                                                        maxlen=max_sequence_length,
                                                                        padding='post')

        next_word_index = np.argmax(model.predict(input_sequence))
        next_word = list(vocabulary)[next_word_index]
        generated_words.append(next_word)

        if next_word == '.':
            break

    generated_response = ' '.join(generated_words).capitalize()

    return predicted_response[0], generated_response

# Test the chatbot
user_prompt = input("User: ")

predicted_response, generated_response = generate_response(user_prompt)
print("Bot (predicted):", predicted_response)
print("Bot (generated):", generated_response)
