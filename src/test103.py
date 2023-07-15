from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np

# Load dataset of user input and bot responses
data = [
    ("Hi, how are you?", "I'm doing well, thank you for asking."),
    ("What's your name?", "I'm an AI chatbot created by OpenAI."),
    ("What can you do?", "I can answer questions, have conversations, and generate text based on prompts."),
]

# Split data into input and output
X = [d[0] for d in data]
y = [d[1] for d in data]

# Tokenize input and output data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X + y)
X = tokenizer.texts_to_sequences(X)
X = pad_sequences(X)
y = tokenizer.texts_to_sequences(y)
y = pad_sequences(y, maxlen=X.shape[1])  # Pad target sequences to match the length of input sequences

# Create model
model = Sequential()
model.add(Embedding(len(tokenizer.word_index) + 1, 128))
model.add(LSTM(128))
model.add(Dense(len(tokenizer.word_index) + 1, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

# Train model on data
model.fit(X, np.array(y), epochs=10)

def generate_sentence(prompt):
    # Tokenize prompt
    prompt = tokenizer.texts_to_sequences([prompt])[0]
    prompt = pad_sequences([prompt], maxlen=X.shape[1])
    
    # Generate next word
    next_word = model.predict_classes(prompt)[0]
    next_word = tokenizer.index_word[next_word]
    
    # Add next word to prompt and repeat until end of sentence
    sentence = [next_word]
    while next_word != '.':
        prompt = tokenizer.texts_to_sequences([sentence])[-1]
        prompt = pad_sequences([prompt], maxlen=X.shape[1])
        next_word = model.predict_classes(prompt)[0]
        next_word = tokenizer.index_word[next_word]
        sentence.append(next_word)
    
    return ' '.join(sentence)


generate_sentence("who are you")
