from skills import Skills
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.callbacks import EarlyStopping

wordnet_lemmatizer = WordNetLemmatizer()
stop_words_eng = set(stopwords.words('english'))

testing = [
    "what do you want to do?",
    "I am board"
]

def preprocess_sentence(sentence):
    sentence = sentence.lower()
    punctuations = "?:!.,;'`´"
    sentence_words = nltk.word_tokenize(sentence)
    lemmatized_sentence = []

    for word in sentence_words:
        if word in punctuations:
            continue
        lemmatized_word = wordnet_lemmatizer.lemmatize(word, pos="v")
        lemmatized_sentence.append(lemmatized_word)

    return " ".join(lemmatized_sentence)

if __name__ == '__main__':
    print("Loading all skills...")
    s = Skills()

    # Load skill sample data
    training_sentences = []
    training_labels = []
    labels = []

    for intent, skill in s.skills.items():
        for sample in skill.samples:
            training_sentences.append(sample)
            training_labels.append(intent)
        if intent not in labels:
            labels.append(intent)

    num_classes = len(labels)

    # Lemmatization for training data
    lemmatized_training_sentences = [preprocess_sentence(sentence) for sentence in training_sentences]

    # Label Encoding and Magic Constants
    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(training_labels)
    training_labels = lbl_encoder.transform(training_labels)

    vocab_size = 2000
    embedding_dim = 32
    max_len = 25
    oov_token = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
    tokenizer.fit_on_texts(lemmatized_training_sentences)
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(lemmatized_training_sentences)
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

    # Hyperparameters for multiple experiments
    early_stopping_patience_values = [10, 20, 30]  # Different patience values for early stopping
    epochs = 5000

    best_val_accuracy = 0.0
    best_experiment_params = None

    testing = [
        ("what do you want to do?", "intent_1"),
        ("I am bored", "intent_2")
    ]

    test_results = {}  # To keep track of test results for each experiment

    for patience_value in early_stopping_patience_values:
        print(f"Experiment with patience value: {patience_value}")

        # Define model
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(num_classes, activation='softmax'))
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.summary()

        # Train the model with early stopping
        early_stopping = EarlyStopping(monitor='val_accuracy', patience=patience_value, restore_best_weights=True)
        history = model.fit(
            padded_sequences, np.array(training_labels),
            verbose=1,
            validation_split=0.1, epochs=epochs,
            callbacks=[early_stopping])

        # Evaluate the model on the validation set
        val_accuracy = max(history.history['val_accuracy'])
        print(f"Validation accuracy: {val_accuracy}")

        # Test the model
        correct_count = 0
        for test_sentence, correct_intent in testing:
            preprocessed_s = preprocess_sentence(test_sentence)
            result = model.predict(pad_sequences(tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
            intent = lbl_encoder.inverse_transform([np.argmax(result)])
            print(test_sentence, intent[0], correct_intent)
            test_results[patience_value] = test_results.get(patience_value, []) + [(test_sentence, intent[0], correct_intent)]

            if intent[0] == correct_intent:
                correct_count += 1

        # Compare with the best result so far (based on both validation accuracy and test results)
        if correct_count > 0 and (val_accuracy > best_val_accuracy or best_experiment_params is None):
            best_val_accuracy = val_accuracy
            best_experiment_params = {
                'patience': patience_value,
                'model': model,
                'correct_count': correct_count
            }
    print(best_experiment_params['patience'])

    # Save the best model and tokenizer
    if best_experiment_params is not None:
        best_model = best_experiment_params['model']
        best_model.save("best_sir-bot-a-lot.brain")
        with open('best_tokenizer.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('best_label_encoder.pickle', 'wb') as ecn_file:
            pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

        print("Best model trained and saved.")
    else:
        print("No model satisfies the validation accuracy and test criteria.")

    # Save the test results for each experiment
    with open('test_results.pickle', 'wb') as tr_file:
        pickle.dump(test_results, tr_file, protocol=pickle.HIGHEST_PROTOCOL)

    # Load the best model and tokenizer for testing
    if best_experiment_params is not None:
        best_model = load_model("best_sir-bot-a-lot.brain")
        with open('best_tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        with open('best_label_encoder.pickle', 'rb') as ecn_file:
            lbl_encoder = pickle.load(ecn_file)

        print("\nTesting: ")
        for test_sentence, correct_intent in testing:
            preprocessed_s = preprocess_sentence(test_sentence)
            result = best_model.predict(pad_sequences(tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
            intent = lbl_encoder.inverse_transform([np.argmax(result)])
            print(test_sentence, "Model's predicted intent:", intent[0], "Correct intent:", correct_intent)
