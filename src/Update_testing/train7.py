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
from tensorflow.keras.callbacks import EarlyStopping, Callback

wordnet_lemmatizer = WordNetLemmatizer()
stop_words_eng = set(stopwords.words('english'))

testing = [
    "what do you want to do?",
    "I am board",
    "What is your favorite holiday?",
    "hi",
    "can you tell me a joke"
]

def preprocess_sentence(sentence):
    sentence = sentence.lower()
    punctuations = "?:!.,;'`´"
    sentence_words = nltk.word_tokenize(sentence)
    lemmatized_sentence = []

    for word in sentence_words:
        #if word in stop_words_eng:
        #     continue
        if word in punctuations:
            continue
        lemmatized_word = wordnet_lemmatizer.lemmatize(word, pos="v")
        lemmatized_sentence.append(lemmatized_word)

    return " ".join(lemmatized_sentence)

class EarlyStoppingByLossVal(Callback):
    def __init__(self, monitor='val_loss', value=0.00001, verbose=0):
        super(Callback, self).__init__()
        self.monitor = monitor
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs={}):
        val_loss = logs.get(self.monitor)
        accuracy = logs.get('accuracy')

        if val_loss == 0.0100:
            print("loss")
            if accuracy == 1.0000:
                if self.verbose > 0:
                    print("Epoch %05d: early stopping THR" % epoch)
                self.model.stop_training = True

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
