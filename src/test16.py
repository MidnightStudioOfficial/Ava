import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import requests

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    return tokens

def similarity(query, title):
    query_tokens = preprocess(query)
    title_tokens = preprocess(title)
    common_tokens = set(query_tokens) & set(title_tokens)
    return len(common_tokens) / len(query_tokens)

def filter_links(query, links, threshold=0.5):
    filtered_links = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        if similarity(query, title) >= threshold:
            filtered_links.append(link)
    return filtered_links
