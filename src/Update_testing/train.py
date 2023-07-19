from skills import Skills

import numpy as np 
#import tensorflow as tf
import pickle
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
#from keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
#from sklearn import preprocessing

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
stop_words_eng = set(stopwords.words('english'))

testing = [
    "what do you want to do?"
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

    # load skill sample data
    training_sentences = []
    training_labels = []
    labels = []
    responses = []
    
    for intent, skill in s.skills.items():
        for sample in skill.samples:
            training_sentences.append(sample)
            training_labels.append(intent)
        if intent not in labels:
            labels.append(intent)

    num_classes = len(labels)

    # Lemmatization
    lemmatized_training_sentences = []
    for sentence in training_sentences:
        sentence = sentence.lower()

        punctuations="?:!.,;'`´"
        sentence_words = nltk.word_tokenize(sentence)
        lemmatized_sentence = []

        for word in sentence_words:
    #        if word in stop_words_eng:
    #            continue
            if word in punctuations:
                continue
            lemmatized_word = wordnet_lemmatizer.lemmatize(word, pos="v")
            print ("{0:20}{1:20}".format(word, lemmatized_word))
            lemmatized_sentence.append(lemmatized_word)
        lemmatized_training_sentences.append(" ".join(lemmatized_sentence))
        # print()


    # Label Encoding and Magic Constants
    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(training_labels)
    training_labels = lbl_encoder.transform(training_labels)

    vocab_size = 1000
    embedding_dim = 16
    max_len = 20
    oov_token = "<OOV>"

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
    tokenizer.fit_on_texts(training_sentences)
    word_index = tokenizer.word_index
    sequences = tokenizer.texts_to_sequences(training_sentences)
    padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
    

    # Define model
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
    model.add(GlobalAveragePooling1D())
    # model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    # train the model and use simple early stopping
    # from keras.callbacks import EarlyStopping
    # es = EarlyStopping(monitor='loss', mode='min', verbose=0, patience=20, min_delta=0.01)

    epochs = 5000
    history = model.fit(
        padded_sequences, np.array(training_labels), 
        verbose=0,
        validation_freq=10, epochs=epochs, 
        workers=1, use_multiprocessing=False) #, callbacks=[es])

    # save the model
    model.save("sir-bot-a-lot.brain")
    # saving tokenizer
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # saving label encoder
    with open('label_encoder.pickle', 'wb') as ecn_file:
        pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

    print("done")
    
    print("Validation: ")
    for s in training_sentences:
        preprocessed_s = preprocess_sentence(s)
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
        intent = lbl_encoder.inverse_transform([np.argmax(result)])
        print(s + " --> " + str(intent[0]))

    print("\nTesting: ")
    for s in testing:
        preprocessed_s = preprocess_sentence(s)
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([preprocessed_s]), truncating='post', maxlen=max_len))
        intent = lbl_encoder.inverse_transform([np.argmax(result)])
        print(s + " --> " + str(intent[0]))
        
    


    # print("Validation: ")
    # for s in training_sentences:
    #     result = model.predict(keras.preprocessing.sequence.pad_sequences(
    #             tokenizer.texts_to_sequences([s]),
    #             truncating='post', maxlen=max_len))
    #     intent = lbl_encoder.inverse_transform([np.argmax(result)])
    #     print(s + " --> " + str(intent))


    # s = "please open vendo dash integration"
    # print(s)
    # result = model.predict(keras.preprocessing.sequence.pad_sequences(
    #         tokenizer.texts_to_sequences([s]),
    #         truncating='post', maxlen=max_len))
    # intent = lbl_encoder.inverse_transform([np.argmax(result)])
    # print(s + " --> " + str(intent))
    # for i in testing:
    #     s = i
    #     print(s)
    #     result = model.predict(keras.preprocessing.sequence.pad_sequences(
    #             tokenizer.texts_to_sequences([s]),
    #             truncating='post', maxlen=max_len))
    #     intent = lbl_encoder.inverse_transform([np.argmax(result)])
    #     print(s + " --> " + str(intent))