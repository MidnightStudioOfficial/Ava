import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyDictionary import PyDictionary

# Initialize NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Function to get synonyms using PyDictionary
def get_synonyms(word):
    dictionary = PyDictionary()
    synonyms = dictionary.synonym(word)
    return synonyms if synonyms else []

# Function to preprocess the sentence
def preprocess(sentence):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(sentence.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return " ".join(lemmatized_tokens)

# Function to check if the sentence is worth changing
def is_worth_changing(original, rewritten):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([original, rewritten])
    similarity_score = cosine_similarity(tfidf_matrix)[0, 1]
    return similarity_score < 0.9  # Tweak this threshold as per your preference

# Main function
def main():
    original_sentence = input("Enter the sentence to be rewritten: ")
    preprocessed_sentence = preprocess(original_sentence)

    words_to_replace = set()
    for word in word_tokenize(preprocessed_sentence):
        synonyms = get_synonyms(word)
        if synonyms:
            words_to_replace.add(word)

    rewritten_sentence = preprocessed_sentence
    for word in words_to_replace:
        synonyms = get_synonyms(word)
        if synonyms:
            rewritten_sentence = rewritten_sentence.replace(word, synonyms[0])  # Replace with the first synonym

    if is_worth_changing(preprocessed_sentence, rewritten_sentence):
        print(f"Original Sentence: {original_sentence}")
        print(f"Rewritten Sentence: {rewritten_sentence}")
    else:
        print("The sentence is not worth changing.")

if __name__ == "__main__":
    main()
