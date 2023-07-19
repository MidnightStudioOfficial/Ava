import numpy as np
import pickle
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from pandas import read_csv
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes

class IntentCheck():

    def __init__(self):
        self.model = keras.models.load_model('sir-bot-a-lot.brain')
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        with open('label_encoder.pickle', 'rb') as enc:
            self.label_encoder = pickle.load(enc)
        # parameters
        self.max_len = 25

    def getIntentFromString(self, text):
        result = self.model.predict(
            keras.preprocessing.sequence.pad_sequences(self.tokenizer.texts_to_sequences([text]),
                                truncating='post', maxlen=self.max_len))
        tag = self.label_encoder.inverse_transform([np.argmax(result)])
        return tag[0]

class ConversationalEngine():

    def __init__(self, lemmatize_data=True, filepath=None, modelpath=None):
        '''
        app: any object | usually the chatbot object
        lemmatize_data: bool | True includes lemmatization, False excludes it
        filepath: str | the path to the .csv file containing the training data
        modelpath str, optional | the path to the .p file containing a pickled model you wish to use. If passed, will use that model instead of retraining from the training data. This leads to faster instantiation.
        '''
        # Read in the training data from a CSV file and sort it by intent name.
        df = read_csv(filepath)
        df.sort_values(by='intent_name')
        
        # Extract the unique intent labels from the training data.
        self.labels = []
        for i in df['intent_name']:
            if i not in self.labels:
                self.labels.append(i)
                
        # Store the training data as a Pandas Series of strings.        
        self.trainingData = df['sample_utterance'].apply(str)
        
        # If no model path is provided, train a new model using the training data.
        if modelpath == None:
            # If lemmatization is enabled, lemmatize the training data using NLTK's WordNetLemmatizer.
            if lemmatize_data==True:
                tag_map = defaultdict(lambda : wn.NOUN)
                tag_map['J'] = wn.ADJ
                tag_map['V'] = wn.VERB
                tag_map['R'] = wn.ADV
                lemmatizer = WordNetLemmatizer()
                df['sample_utterance'] = df['sample_utterance'].apply(self._lemmatize, tagMap=tag_map, ignoreStopWords=True, lemmatizer=lemmatizer)
                
            # Tokenize the training data using NLTK's word_tokenize function.
            df['sample_utterance'] = [word_tokenize(entry) for entry in df['sample_utterance']]
            
            # Vectorize the training data using scikit-learn's TfidfVectorizer.
            self.Tfidf_vectored = TfidfVectorizer(max_features=5000)
            self.Tfidf_vectored.fit(self.trainingData)
            Train_X_Tfidf = self.Tfidf_vectored.transform(self.trainingData)
            
             # Train a Naive Bayes classifier on the vectorized training data.
            self.Naive = naive_bayes.MultinomialNB()
            self.Naive.fit(Train_X_Tfidf, df['intent_name'])
        # If a model path is provided, load an existing model from a pickled file.
        else: 
            import pickle
            self.Naive=pickle.load( open( modelpath, "rb" ))
    
    def getIntent(self, utterance):
        '''
        arguments:
            utterance: str | the utterance entered by the user

        returns: 
            a dictionary containing the following key-value pairs:
            intent: str -- the predicted intent
            probability -- float | the probability score for that intent 
            probability_matrix -- list | a 2-dimensional list with elements of [intent name, probability] for all intents in the training set, sorted by highest to lowest probability
        '''
        # Vectorize the input utterance using scikit-learn's TfidfVectorizer.
        vectorizer = TfidfVectorizer(max_features=5000)
        vectorizer.fit(self.trainingData)
        vectored_transformed = vectorizer.transform([utterance])
        
        # Use the trained Naive Bayes classifier to predict the intent of the input utterance and calculate its probabilities.
        predictions_NB = self.Naive.predict(vectored_transformed)
        score = self.Naive.predict_proba(vectored_transformed)
        probability_matrix = sorted(zip(self.Naive.classes_, score[0]), key=lambda x: x[1], reverse=True)
        
        # Return the predicted intent and associated probabilities.
        return {
            'intent': predictions_NB[0],
            'probability': sorted(score[0], reverse=True)[0],
            'probability_matrix': probability_matrix
        }
        
    # This method lemmatizes a given input string using NLTK's WordNetLemmatizer.
    def _lemmatize(self, value, tagMap, ignoreStopWords, lemmatizer):
        # Initialize an empty list to store the lemmatized words.
        outputList = []
        
        # Convert the input value to a string and strip any enclosing square brackets or single quotes.
        word = str(value).strip("'[]")
        
        # Tokenize the input string using NLTK's word_tokenize function.
        word = word_tokenize(value)
        
        # Iterate over each word and its part-of-speech tag in the tokenized input string.
        for word, tag in pos_tag(word):
            # If the word is not a stopword (or if ignoring stopwords is disabled) and the word is alphabetic,
            # lemmatize the word using NLTK's WordNetLemmatizer and the provided tag map.
            if (word not in stopwords.words('english') or ignoreStopWords==False) and word.isalpha():
                word_Final = lemmatizer.lemmatize(word, tagMap[tag[0]])
                outputList.append(word_Final)
                
        # Delete the original input value to free up memory.
        del word
        
        # Return the list of lemmatized words as a string.
        return str(outputList)
    
    def pickleModel(self, path):
        '''pickles the conversation's trained model into a .p file at the defined path.
        Path should include filename. for example: "folder\model.p"'''
        import pickle
        pickle.dump(self.Naive, open( path, "wb"))

    def predict_intent(self, text, threshold=0.5):
        # Combine both models to predict the intent of the text
        intent_check = IntentCheck()
        intent_keras = intent_check.getIntentFromString(text)
        intent_naive_bayes = self.getIntent(text)

        # Get the probabilities from both models
        prob_keras = intent_check.model.predict(
            keras.preprocessing.sequence.pad_sequences(intent_check.tokenizer.texts_to_sequences([text]),
                                                       truncating='post', maxlen=intent_check.max_len))
        prob_naive_bayes = self.Naive.predict_proba(self.Tfidf_vectored.transform([text]))

        # Determine the most likely intent based on probabilities
        combined_intent = None
        combined_probability = 0.0

        # Check if both models agree on the same intent
        if intent_keras == intent_naive_bayes:
            combined_intent = intent_keras
            combined_probability = max(np.max(prob_keras), np.max(prob_naive_bayes))

        # If models disagree or have low confidence, use some criteria to handle the situation
        else:
            # For example, you can choose the model with the highest probability
            if np.max(prob_keras) > np.max(prob_naive_bayes):
                combined_intent = intent_keras
                combined_probability = np.max(prob_keras)
            else:
                combined_intent = intent_naive_bayes
                combined_probability = np.max(prob_naive_bayes)

        # You can also use a threshold to decide when to use one model over the other
        if combined_probability < threshold:
            combined_intent = "Unknown"

        return {
            'intent': combined_intent,
            'probability': combined_probability,
            'np.max(prob_keras)': str(np.max(prob_keras))
        }

# Usage example:
engine = ConversationalEngine(filepath='../Data/training.csv')
result = engine.predict_intent('can you tell me a joke')
print(result)
