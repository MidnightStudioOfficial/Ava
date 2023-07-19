import numpy as np
import pickle
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder


class IntentCheck():

    def __init__(self):
        self.model = keras.models.load_model('sir-bot-a-lot.brain')
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open('label_encoder.pickle', 'rb') as enc:
            self.label_encoder = pickle.load(enc)
        # parameters
        self.max_len = 20

    def getIntentFromString(self, text):
        result = self.model.predict(
            keras.preprocessing.sequence.pad_sequences(self.tokenizer.texts_to_sequences([text]),
                                truncating='post', maxlen=self.max_len))
        tag = self.label_encoder.inverse_transform([np.argmax(result)])
        # TODO: Only the max probability intent is returned. It may be wise to have a skill 'unknown' based on some probability.
        return tag[0]
