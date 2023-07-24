"""
Conversational Engine using a Neural Network

This script defines a conversational engine that can predict the intent of an utterance using a neural network.
The engine uses deep learning techniques to classify user input into predefined intents, enabling it to respond
with appropriate actions or responses. It leverages libraries such as TensorFlow, Keras, NLTK, and spaCy for NLP
functionalities and model training.

The Engine2 class includes methods for intent prediction, data preprocessing, model training, and skill management.
It utilizes labeled training data with corresponding intents to train a neural network and uses a Tokenizer for text
preprocessing. The engine also incorporates built-in skills for handling various user requests.

Note: This implementation is part of a larger project and may have specific dependencies on the rest of the codebase.
"""
# Standard libraries
import os  # For interacting with the operating system (e.g., checking file existence)
import pickle  # For pickling (serializing) Python objects

# Third-party libraries
from numpy import max, argmax, array as np_max, argmax, array  # NumPy for numerical operations and array handling
from nltk import word_tokenize  # Natural Language Toolkit for NLP functionalities
from nltk.corpus import stopwords  # NLTK's stopwords for filtering common words
from nltk.stem import WordNetLemmatizer  # WordNetLemmatizer for word lemmatization
from spacy import load as spacy_load  # spaCy for advanced natural language processing

# TensorFlow and Keras libraries
from tensorflow import keras  # TensorFlow library for deep learning
from tensorflow.keras.models import Sequential, load_model  # Keras's Sequential model for creating neural networks
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D  # Keras layers for building the neural network architecture
from tensorflow.keras.preprocessing.text import Tokenizer  # Tokenizer for text preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences  # Padding sequences for input data
from tensorflow.keras.callbacks import EarlyStopping  # EarlyStopping callback for stopping training early

# Third-party library
from sklearn.preprocessing import LabelEncoder  # LabelEncoder for encoding target labels
from sklearn.model_selection import train_test_split  # train_test_split for splitting data into training and testing sets
from nltk.stem import PorterStemmer  # PorterStemmer for word stemming (reducing words to their base or root form)

# Local import
from core.skill.bulitin_skills import BuiltinSkills  # Custom built-in skills for the conversational engine


# This class defines a conversational engine that can predict the intent of an utterance using a neural network.
class Engine2():
    # The constructor takes in several optional arguments to customize the behavior of the engine.
    def __init__(self, lemmatize_data=True, filepath=None, modelpath=None):
        """
        app: any object | usually the chatbot object
        lemmatize_data: bool | True includes lemmatization, False excludes it
        filepath: str | the path to the .csv file containing the training data
        modelpath str, optional | the path to the .p file containing a pickled model you wish to use. If passed, will use that model instead of retraining from the training data. This leads to faster instantiation.
        """
        if os.path.exists('Data/sir-bot-a-lot.brain') and os.path.exists('Data/tokenizer.pickle') and os.path.exists('Data/label_encoder.pickle'):
            # Load the pre-trained model and associated objects
            self.model = keras.models.load_model('Data/sir-bot-a-lot.brain')
            with open('Data/tokenizer.pickle', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            with open('Data/label_encoder.pickle', 'rb') as enc:
                self.label_encoder = pickle.load(enc)
        else:
            # Set up data preprocessing and train the model
            self.testing = [
                "what do you want to do?",
                "I am board",
                "What is your favorite holiday?",
                "hi",
                "can you tell me a joke"
            ]
            self.testing2 = [
                "what do you want to do?",
                "I am board",
                "What is your favorite holiday?",
                "hi",
                "can you tell me a joke",
                "can you get the weather",

                "can you play me some music"
            ]
            # WordNetLemmatizer is used to reduce words to their base or root form (lemmas).
            # It helps to normalize different forms of a word, such as plurals or verb conjugations, to a common base form.
            self.wordnet_lemmatizer = WordNetLemmatizer()

            # Create an instance of the PorterStemmer class for stemming words.
            # The PorterStemmer is used to reduce words to their base or root form, which can help in information retrieval or text analysis tasks.
            self.porter_stemmer = PorterStemmer()

            # Initialize the set of English stopwords, which are common words that are usually removed from text during preprocessing.
            # Stopwords are words like "the", "and", "is", "are", etc., that do not contribute much to the meaning of the text.
            self.stop_words_eng = set(stopwords.words('english'))
            self.stop_words_eng.remove("what")
            self.train2()

        # Define parameters
        self.max_len = 25

        # Load built-in skills for the engine
        self.skills = BuiltinSkills()

        # Load the spaCy language model for natural language processing
        self.nlp = spacy_load("en_core_web_sm")

    def getIntent(self, utterance):
        """
        Predicts the intent of an utterance using the neural network.

        Parameters:
            utterance (str): The utterance entered by the user.

        Returns:
            dict: A dictionary containing the following key-value pairs:
                  'intent' (str): The predicted intent.
                  'probability' (float): The probability score for the predicted intent.
        """
        # Predict the intent using the neural network model
        result = self.model.predict(
            keras.preprocessing.sequence.pad_sequences(self.tokenizer.texts_to_sequences([utterance]),
                                truncating='post', maxlen=self.max_len))

        # Convert prediction to human-readable intent
        tag = self.label_encoder.inverse_transform([argmax(result)])
        # TODO: Only the max probability intent is returned. It may be wise to have a skill 'unknown' based on some probability.

        # Initialize standard set of parameters for skill parsing
        params = {'intentCheck': tag, 'skills': self.skills.skills}

        # Get the corresponding skill based on the predicted intent
        skill = self.skills.skills[tag[0]]

        # Parse entities from the utterance using spaCy
        params |= skill.parseEntities(self.nlp(utterance))

        # Get the response from the skill based on the parsed entities
        response = skill.actAndGetResponse(**params)
        print(response)

        # Return the predicted intent and associated probabilities.
        return {
            'intent': response,
            'probability': np_max(result)
        }

    def preprocess_sentence(self, sentence):
        sentence = sentence.lower()
        punctuations = "?:!.,;'`´"
        sentence_words = word_tokenize(sentence)
        lemmatized_sentence = []

        for word in sentence_words:
            #if word in stop_words_eng:
            #     continue
            if word in punctuations:
                continue
            lemmatized_word = self.wordnet_lemmatizer.lemmatize(word, pos="v")
            lemmatized_sentence.append(lemmatized_word)

        return " ".join(lemmatized_sentence)

    def preprocess_sentence2(self, sentence):
        """
        Preprocesses a sentence using stemming and removes stopwords and punctuations.

        Parameters:
            sentence (str): The input sentence to preprocess.

        Returns:
            str: The preprocessed sentence after stemming and removing stopwords and punctuations.
        """
        # Convert the sentence to lowercase for consistency
        sentence = sentence.lower()

        # Define a string of punctuations to ignore
        punctuations = "?:!.,;'`´"

        # Tokenize the sentence into individual words
        sentence_words = word_tokenize(sentence)

        # Initialize a list to store stemmed words
        stemmed_sentence = []

        # Loop through each word in the tokenized sentence
        for word in sentence_words:
            # Skip the word if it is a common English stopword
            if word in self.stop_words_eng:
                continue

            # Skip the word if it is a punctuation
            if word in punctuations:
                continue

            # Apply stemming to the word to get the root form
            stemmed_word = self.porter_stemmer.stem(word)
            stemmed_sentence.append(stemmed_word)

        # Return the preprocessed sentence as a string
        return " ".join(stemmed_sentence)

    def train2(self):
        """
        Train the neural network model for intent classification.

        This method performs the following steps:
        1. Load skill sample data.
        2. Preprocess the training data (lemmatization).
        3. Encode the labels using LabelEncoder.
        4. Prepare the data for training, validation, and testing using train_test_split.
        5. Define the neural network model architecture.
        6. Train the model using early stopping.
        7. Evaluate the model on the test set.
        8. Save the trained model and tokenizer for later use.
        """
        print("Loading all skills...")
        s = self.skills

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
        lemmatized_training_sentences = [self.preprocess_sentence2(sentence) for sentence in training_sentences]

        # Label Encoding and Magic Constants
        lbl_encoder = LabelEncoder()
        lbl_encoder.fit(training_labels)
        training_labels = lbl_encoder.transform(training_labels)

        vocab_size = 2000  # Vocabulary size for the Tokenizer
        embedding_dim = 62  # Dimension of word embeddings
        max_len = 25  # Maximum length of input sequences
        oov_token = "<OOV>"  # Out-of-vocabulary token for the Tokenizer

        # Initialize a Tokenizer object with vocabulary size and OOV token
        tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)

        # Fit the Tokenizer on lemmatized training sentences to build the word-to-index mapping
        tokenizer.fit_on_texts(lemmatized_training_sentences)

        # Get the word index, which maps each word in the vocabulary to a unique index
        word_index = tokenizer.word_index

        # Convert lemmatized training sentences to sequences of integers based on the tokenizer's word-to-index mapping
        sequences = tokenizer.texts_to_sequences(lemmatized_training_sentences)

        # Pad the sequences to ensure they have the same length (max_len) for neural network input
        padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

        # Split data into training, validation, and test sets
        X_train, X_temp, y_train, y_temp = train_test_split(padded_sequences, array(training_labels), test_size=0.2, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

        # Define model architecture
        model = Sequential()
        model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(128, activation='relu'))  # Hidden layer with 128 units and ReLU activation
        model.add(Dense(32, activation='relu'))   # Hidden layer with 32 units and ReLU activation
        model.add(Dense(num_classes, activation='softmax'))  # Output layer with 'num_classes' units for classification
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.summary()

        # Train the model with early stopping
        epochs = 1000  # Maximum number of training epochs
        early_stopping = EarlyStopping(monitor='val_loss', patience=100, restore_best_weights=True)
        history = model.fit(
            X_train, y_train,
            verbose=1,
            batch_size=32,
            validation_split=0.1, epochs=epochs,
            validation_data=(X_val, y_val),  # Use validation data for early stopping
            callbacks=[early_stopping]
        )

        # Evaluate the model on the test set
        loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
        print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

        # Save the trained model and tokenizer
        model.save("Data/sir-bot-a-lot.brain")
        with open('Data/tokenizer.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('Data/label_encoder.pickle', 'wb') as ecn_file:
            pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

        print("Model trained and saved.")

        # Load the model and tokenizer for testing
        self.model = load_model("Data/sir-bot-a-lot.brain")
        with open('Data/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open('Data/label_encoder.pickle', 'rb') as ecn_file:
            self.label_encoder = pickle.load(ecn_file)

        # Perform testing on some sample sentences
        print("\nTesting: ")
        for s in self.testing2:
            preprocessed_s = self.preprocess_sentence2(s)
            result = self.model.predict(pad_sequences(self.tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
            intent = self.label_encoder.inverse_transform([argmax(result)])
            print(s + " --> " + str(intent[0]))

    def train(self):
        print("Loading all skills...")
        s = BuiltinSkills()

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
        lemmatized_training_sentences = [self.preprocess_sentence(sentence) for sentence in training_sentences]

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
        epochs = 5000
        early_stopping = EarlyStopping(monitor='val_loss', patience=100, restore_best_weights=True) # patience=10 30
        early_stopping = EarlyStopping(monitor='val_accuracy', patience=156, restore_best_weights=True, mode="max") # , patience=100, mode="min"
        #early_stopping = EarlyStoppingByLossVal(monitor='val_loss', value=0.0090, verbose=1)
        #early_stopping = EarlyStopping(monitor='val_loss', patience=156, restore_best_weights=True, min_delta=0.001, mode='max')
        history = model.fit(
            padded_sequences, array(training_labels),
            verbose=1,
            batch_size=32,
            validation_split=0.1, epochs=epochs,
            callbacks=[early_stopping])

        # Save the model and tokenizer
        model.save("Data/sir-bot-a-lot.brain")
        with open('Data/tokenizer.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('Data/label_encoder.pickle', 'wb') as ecn_file:
            pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

        print("Model trained and saved.")

        # Load the model and tokenizer for testing
        self.model = load_model("Data/sir-bot-a-lot.brain")
        with open('Data/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open('Data/label_encoder.pickle', 'rb') as ecn_file:
            self.label_encoder = pickle.load(ecn_file)

        print("\nTesting: ")
        for s in self.testing:
            preprocessed_s = self.preprocess_sentence(s)
            result = self.model.predict(pad_sequences(self.tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
            intent = self.label_encoder.inverse_transform([argmax(result)])
            print(s + " --> " + str(intent[0]))
