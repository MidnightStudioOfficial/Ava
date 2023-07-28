from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class ReferencingClassifier:
    """A classifier that predicts whether a user is referring to themselves or the chatbot."""

    def __init__(self) -> None:
        """
        Initializes the classifier.

        Creates a dataset of labeled data and splits it into training and testing sets.
        Also creates a TF-IDF vectorizer and a MultinomialNB classifier.
        """
        # Sample labeled data for training the classifier
        self.labeled_data = [
            ("I need your help", "user"),
            ("What can you do for me?", "user"),
            ("How are you?", "chatbot"),
            ("Tell me a joke", "user"),
            ("You are very helpful", "chatbot"),
            ("I am feeling happy", "user"),
            ("Can you provide some information?", "user"),
            ("You are doing a great job!", "chatbot"),
        ]
        # Separate the input (X) and labels (y)
        self.X, self.y = zip(*self.labeled_data)

        # Convert the input text to TF-IDF features
        self.tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenize, lowercase=True) #, sublinear_tf=True
        self.classifier = MultinomialNB()

    def train(self) -> None:
        """Trains the classifier on a dataset of labeled data."""
        self.X_tfidf = self.tfidf_vectorizer.fit_transform(self.X)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(self.X_tfidf, self.y, test_size=0.2, random_state=42)

        self.classifier.fit(X_train, y_train)

        # Make predictions on the test set
        self.y_pred = self.classifier.predict(X_test)

        # Calculate accuracy on the test set
        self.accuracy = accuracy_score(y_test, self.y_pred)
        print("Classifier accuracy:", self.accuracy)

    def predict(self, input_text: str):
        """Makes a prediction on a new input text.

        Args:
            input_text (str): The input text to be classified.

        Returns:
            str: The predicted label.
        """
        if not input_text.strip():
            raise ValueError("Input text is empty.")

        user_input_tfidf = self.tfidf_vectorizer.transform([input_text])
        prediction = self.classifier.predict(user_input_tfidf)[0]
        return prediction
