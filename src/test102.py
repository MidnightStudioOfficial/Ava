import random
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

# Sample training dataset
dataset = [
    ("How are you?", "I'm fine, thank you."),
    ("What's your name?", "I am ChatBot."),
    # Add more training examples
]

# Preprocess the dataset
nltk.download('punkt')

questions = []
answers = []

for question, answer in dataset:
    questions.append(question)
    answers.append(answer)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers)

question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

vocab_size = len(tokenizer.word_index) + 1

X = []
y = []

for i in range(len(question_sequences)):
    for j in range(1, len(question_sequences[i])):
        X.append(question_sequences[i][:j])
        y.append(question_sequences[i][j])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train = tokenizer.sequences_to_matrix(X_train, mode='binary')
X_test = tokenizer.sequences_to_matrix(X_test, mode='binary')

y_train = to_categorical(y_train, num_classes=vocab_size)
y_test = to_categorical(y_test, num_classes=vocab_size)

# Build and train the model
model = Sequential()
model.add(Dense(256, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=100, batch_size=64, verbose=1)

# Generate responses
def generate_response(prompt):
    prompt_sequence = tokenizer.texts_to_sequences([prompt])
    input_sequence = tokenizer.sequences_to_matrix(prompt_sequence, mode='binary')

    predicted_sequence = model.predict(input_sequence)
    predicted_token = tokenizer.index_word[np.argmax(predicted_sequence)]

    return predicted_token

# Example usage
while True:
 user_input = input("User: ")
 response = generate_response(user_input)
 print("ChatBot:", response)
