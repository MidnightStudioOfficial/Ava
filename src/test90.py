import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk


def search_bing(query):
    url = f"https://www.bing.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('li', class_='b_algo')
    return results

def scrape_results(results):
    extracted_results = []
    for result in results:
        title = result.find('h2').get_text()
        url = result.find('a')['href']
        snippet = result.find('p').get_text()
        extracted_results.append({'title': title, 'url': url, 'snippet': snippet})
    return extracted_results

def summarize_text(text):
    sentences = sent_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in nltk.word_tokenize(text) if word.isalpha() and word.lower() not in stop_words]

    # Check if there are valid words left after stop word removal
    if not words:
        return ""

    # Calculate word frequency
    word_frequency = FreqDist(words)

    # Calculate TF-IDF scores
    tfidf = TfidfVectorizer()
    tfidf_scores = tfidf.fit_transform(sentences)

    # Calculate sentence scores based on TF-IDF scores
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequency.keys() and word in tfidf.vocabulary_:
                if len(sentence.split()) < 30:
                    if i in sentence_scores.keys():
                        sentence_scores[i] += tfidf_scores[i, tfidf.vocabulary_[word]]
                    else:
                        sentence_scores[i] = tfidf_scores[i, tfidf.vocabulary_[word]]

    # Get top 3 sentences with highest scores
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:4] #[:3]
    summary = [sentences[i] for i in summary_sentences]

    return ' '.join(summary)

def main():
    query = input("Enter your search query (make sure your search query has no miss spellings): ")
    search_results = search_bing(query)
    extracted_results = scrape_results(search_results)

    # Print extracted information
    print("\nExtracted Results:")
    for result in extracted_results:
        print("Title:", result['title'])
        print("URL:", result['url'])
        # print("Snippet:", result['snippet'])
        print()

    # Combine snippets for summarization
    combined_snippets = ' '.join(result['snippet'] for result in extracted_results)

    summary = summarize_text(combined_snippets)
    print("\nSummary:")
    print(summary)

if __name__ == "__main__":
    main()
