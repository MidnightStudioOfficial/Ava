import numpy as np
import pickle
import os
import nltk
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping

from core.skill.bulitin_skills import BuiltinSkills
import spacy


# This class defines a conversational engine that can predict the intent of an utterance using a nural network.
class Engine2():
    # The constructor takes in several optional arguments to customize the behavior of the engine.
    def __init__(self, lemmatize_data=True, filepath=None, modelpath=None):
        '''
        app: any object | usually the chatbot object
        lemmatize_data: bool | True includes lemmatization, False excludes it
        filepath: str | the path to the .csv file containing the training data
        modelpath str, optional | the path to the .p file containing a pickled model you wish to use. If passed, will use that model instead of retraining from the training data. This leads to faster instantiation.
        '''
        if os.path.exists('Data/sir-bot-a-lot.brain') and os.path.exists('Data/tokenizer.pickle') and os.path.exists('Data/label_encoder.pickle'):
            # Read in the training data from a CSV file and sort it by intent name.
            self.model = keras.models.load_model('Data/sir-bot-a-lot.brain')
            with open('Data/tokenizer.pickle', 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            with open('Data/label_encoder.pickle', 'rb') as enc:
                self.label_encoder = pickle.load(enc)
        else:
            self.testing = [
                "what do you want to do?",
                "I am board",
                "What is your favorite holiday?",
                "hi",
                "can you tell me a joke"
            ]
            self.wordnet_lemmatizer = WordNetLemmatizer()
            self.stop_words_eng = set(stopwords.words('english'))
            self.train()
        # parameters
        self.max_len = 25
        # load skills
        self.skills = BuiltinSkills()
        self.nlp = spacy.load("en_core_web_sm")
    
    def getIntent(self, utterance):
        '''
        arguments:
            utterance: str | the utterance entered by the user

        returns: 
            a dictionary containing the following key-value pairs:
            intent: str -- the predicted intent
            probability -- float | the probability score for that intent 
        '''
        result = self.model.predict(
            keras.preprocessing.sequence.pad_sequences(self.tokenizer.texts_to_sequences([utterance]),
                                truncating='post', maxlen=self.max_len))
        tag = self.label_encoder.inverse_transform([np.argmax(result)])
        # TODO: Only the max probability intent is returned. It may be wise to have a skill 'unknown' based on some probability.
        

        # initialize standard set of parameters
        params = {'intentCheck': tag, 'skills': self.skills.skills} 

        skill = self.skills.skills[tag[0]]
        params |= skill.parseEntities(self.nlp(utterance))

        response = skill.actAndGetResponse(**params)
        print(response)
        
        # Return the predicted intent and associated probabilities.
        return {
            'intent': response,
            'probability': np.max(result)
        }
        
    def preprocess_sentence(self, sentence):
        sentence = sentence.lower()
        punctuations = "?:!.,;'`´"
        sentence_words = nltk.word_tokenize(sentence)
        lemmatized_sentence = []

        for word in sentence_words:
            #if word in stop_words_eng:
            #     continue
            if word in punctuations:
                continue
            lemmatized_word = self.wordnet_lemmatizer.lemmatize(word, pos="v")
            lemmatized_sentence.append(lemmatized_word)

        return " ".join(lemmatized_sentence)
    
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
            padded_sequences, np.array(training_labels),
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
            intent = self.label_encoder.inverse_transform([np.argmax(result)])
            print(s + " --> " + str(intent[0]))





