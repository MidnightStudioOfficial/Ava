from pandas import read_csv
#from sklearn import preprocessing
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes #, svm, model_selection
#from sklearn.metrics import accuracy_score


# This class defines a conversational engine that can predict the intent of an utterance using a Naive Bayes classifier.
class ConversationalEngine():
    # The constructor takes in several optional arguments to customize the behavior of the engine.
    def __init__(self, lemmatize_data=True, filepath=None, modelpath=None):
        """
        app: any object | usually the chatbot object
        lemmatize_data: bool | True includes lemmatization, False excludes it
        filepath: str | the path to the .csv file containing the training data
        modelpath str, optional | the path to the .p file containing a pickled model you wish to use. If passed, will use that model instead of retraining from the training data. This leads to faster instantiation.
        """
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
            if lemmatize_data == True:
                tag_map = defaultdict(lambda : wn.NOUN)
                tag_map['J'] = wn.ADJ
                tag_map['V'] = wn.VERB
                tag_map['R'] = wn.ADV
                lemmatizer = WordNetLemmatizer()
                df['sample_utterance'] = df['sample_utterance'].apply(self._lemmatize, tagMap=tag_map, ignoreStopWords=True, lemmatizer=lemmatizer)

            # Tokenize the training data using NLTK's word_tokenize function.
            df['sample_utterance'] = [word_tokenize(entry) for entry in df['sample_utterance']]

            # Vectorize the training data using scikit-learn's TfidfVectorizer.
            Tfidf_vectored = TfidfVectorizer(max_features=5000)
            Tfidf_vectored.fit(self.trainingData)
            Train_X_Tfidf = Tfidf_vectored.transform(self.trainingData)
            
            # Train a Naive Bayes classifier on the vectorized training data.
            self.Naive = naive_bayes.MultinomialNB()
            self.Naive.fit(Train_X_Tfidf, df['intent_name'])
        # If a model path is provided, load an existing model from a pickled file.
        else:
            import pickle
            self.Naive = pickle.load(open( modelpath, "rb" ))

    def getIntent(self, utterance):
        """
        arguments:
            utterance: str | the utterance entered by the user

        returns: 
            a dictionary containing the following key-value pairs:
            intent: str -- the predicted intent
            probability -- float | the probability score for that intent
            probability_matrix -- list | a 2-dimensional list with elements of [intent name, probability] for all intents in the training set, sorted by highest to lowest probability
        """
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
            if (word not in stopwords.words('english') or ignoreStopWords == False) and word.isalpha():
                word_Final = lemmatizer.lemmatize(word, tagMap[tag[0]])
                outputList.append(word_Final)

        # Delete the original input value to free up memory.
        del word

        # Return the list of lemmatized words as a string.
        return str(outputList)

    def pickleModel(self, path):
        """pickles the conversation's trained model into a .p file at the defined path.
        Path should include filename. for example: folder\model.p"""
        import pickle
        pickle.dump(self.Naive, open(path, "wb"))
