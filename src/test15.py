import requests
from bs4 import BeautifulSoup
from googlesearch import search
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import urllib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import time

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
        try:
            print("filtering: " + str(link))
            response = requests.get(link)
            print("filtering get ")
            soup = BeautifulSoup(response.text, 'html.parser')
            print("filtering soup ")
            title = soup.find('title')
            if title is not None and similarity(query, title.text) >= threshold:
                filtered_links.append(link)
        except requests.exceptions.ConnectionError:
            print(f'Error connecting to {link}. Skipping...')
        except Exception as e:
            print(f'Error processing {link}: {e}')
    return filtered_links


def search_bing(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f'https://www.bing.com/search?q={query}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('li', class_='b_algo')
    links = [result.find('a')['href'] for result in results]
    return links

def search_google2(query):
    while True:
        try:
            links = [j for j in search(query, num=5)]
            return links
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print('Too many requests. Waiting for 1 second...')
                time.sleep(1)
            else:
                raise e


def search_google(query):
    links = [j for j in search(query, num=1)]  # num=10
    return links

def summarize(url):
    try:
     LANGUAGE = 'english'
     SENTENCES_COUNT = 2 #3
     parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
     stemmer = Stemmer(LANGUAGE)
     summarizer = Summarizer(stemmer)
     summarizer.stop_words = get_stop_words(LANGUAGE)
     summary = summarizer(parser.document, SENTENCES_COUNT)
    except requests.exceptions.HTTPError as e:
        print(f'Error fetching {url}: {e}')
        return ''
    return ' '.join([str(sentence) for sentence in summary])

def rank_summaries(query, summaries):
    ranked_summaries = sorted(summaries, key=lambda x: similarity(query, x), reverse=True)
    return ranked_summaries


def main():
    query = input('Enter your search query: ')
    print(f'Query: {query}')
    bing_links = search_bing(query)
    print(f'Bing links: {bing_links}')
    # google_links = search_google2(query)
    # print(f'Google links: {google_links}')
    all_links_OLD = list(set(bing_links)) # + google_links list(set(bing_links))
    all_links = []
    for i in all_links_OLD:
        if str(i).endswith('/') == False:
           # print(str(i)+ str(i).endswith('/'))
            all_links.append(str(i)+'/')
        else:
           # print(str(i))
            all_links.append(str(i))

    print(f'All links: {all_links}')
    print(f'Found {len(all_links)} links. Filtering...')
    new_links = filter_links(query, all_links)
    print(f'{len(new_links)} links remaining. Summarizing...')
    summaries = [summarize(link) for link in new_links]
    combined_summary = ' '.join(summaries)
    ranked_summaries = rank_summaries(query, summaries)
    combined_summary = ' '.join(ranked_summaries)
    print(combined_summary)

if __name__ == '__main__':
    main()
