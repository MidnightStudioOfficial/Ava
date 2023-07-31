from nltk import word_tokenize  # Natural Language Toolkit for NLP functionalities
from nltk.corpus import stopwords  # NLTK's stopwords for filtering common words
from nltk.stem import WordNetLemmatizer  # WordNetLemmatizer for word lemmatization
from nltk.stem import PorterStemmer  # PorterStemmer for word stemming (reducing words to their base or root form)


class TextPreprocessor:
    def __init__(self) -> None:
        self.wordnet_lemmatizer = WordNetLemmatizer()

        # Create an instance of the PorterStemmer class for stemming words.
        # The PorterStemmer is used to reduce words to their base or root form, which can help in information retrieval or text analysis tasks.
        self.porter_stemmer = PorterStemmer()

        # Initialize the set of English stopwords, which are common words that are usually removed from text during preprocessing.
        # Stopwords are words like "the", "and", "is", "are", etc., that do not contribute much to the meaning of the text.
        self.stop_words_eng = set(stopwords.words('english'))
        self.stop_words_eng.remove("what")

    def preprocess_sentence(self, sentence: str):
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

    def preprocess_sentence_2(self, sentence: str):
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
