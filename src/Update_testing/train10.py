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
#from tensorflow.random import set_seed
from sklearn.model_selection import train_test_split
from nltk.stem import PorterStemmer
from tensorflow.keras.regularizers import l1, l2

from tensorflow.keras.layers import LSTM

wordnet_lemmatizer = WordNetLemmatizer()
stop_words_eng = set(stopwords.words('english'))

testing = [
    "what do you want to do?",
    "I am board",
    "What is your favorite holiday?",
    "hi",
    "can you tell me a joke",
    "can you get the weather"
]

# Set random seeds for reproducibility (optional)
#np.random.seed(42)
#set_seed(42)


# ... (existing code)

# Initialize the Porter Stemmer
porter_stemmer = PorterStemmer()

# Replace the existing stopword list with the NLTK English stopword list
stop_words_eng = set(stopwords.words('english'))

# Modify the preprocess_sentence function
def preprocess_sentence(sentence):
    sentence = sentence.lower()
    punctuations = "?:!.,;'`´"
    sentence_words = nltk.word_tokenize(sentence)
    stemmed_sentence = []

    for word in sentence_words:
        if word in stop_words_eng:
            continue
        if word in punctuations:
            continue
        stemmed_word = porter_stemmer.stem(word)  # Use stemming instead of lemmatization
        stemmed_sentence.append(stemmed_word)

    #print(stemmed_sentence)
    return " ".join(stemmed_sentence)

# ... (rest of the code, including model training and testing)


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
 
    vocab_size = 2000 #2000
    embedding_dim = 62 #32
    max_len = 25
    oov_token = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
    tokenizer.fit_on_texts(lemmatized_training_sentences)
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(lemmatized_training_sentences)
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
    
    X_train, X_temp, y_train, y_temp = train_test_split(padded_sequences, np.array(training_labels), test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Define model
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
    model.add(GlobalAveragePooling1D())
    #model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01))) # Adding L2 regularization 64
    #model.add(Dense(32, activation='relu', kernel_regularizer=l1(0.01))) # Adding L1 regularization
    model.add(Dense(128, activation='relu')) # Adding L2 regularization 64
    model.add(Dense(32, activation='relu')) # Adding L1 regularization
    model.add(Dense(num_classes, activation='softmax'))  # Output layer with appropriate number of units for classification
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()


    # Train the model with early stopping
    early_stopping_monitors = ['val_loss', 'val_accuracy', 'loss']

    for monitor in early_stopping_monitors:
            print(f"\nTesting EarlyStopping with monitor: {monitor}")

            # Train the model with early stopping
            epochs = 1000 #5000
            early_stopping = EarlyStopping(monitor=monitor, patience=100, restore_best_weights=True)
            history = model.fit(
                X_train, y_train,
                verbose=1,
                batch_size=32,
                validation_split=0.1, epochs=epochs,
                validation_data=(X_val, y_val),
                callbacks=[early_stopping]
            )

            loss, accuracy = model.evaluate(X_test, y_test, verbose=1) 
            print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

    print("Model training and evaluation with different EarlyStopping monitors completed.")

    # Save the model and tokenizer
    model.save("sir-bot-a-lot.brain")
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('label_encoder.pickle', 'wb') as ecn_file:
        pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

    print("Model trained and saved.")

    # Load the model and tokenizer for testing
    model = load_model("sir-bot-a-lot.brain")
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('label_encoder.pickle', 'rb') as ecn_file:
        lbl_encoder = pickle.load(ecn_file)

    print("\nTesting: ")
    for s in testing:
        preprocessed_s = preprocess_sentence(s)
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
        intent = lbl_encoder.inverse_transform([np.argmax(result)])
        print(s + " --> " + str(intent[0]))
