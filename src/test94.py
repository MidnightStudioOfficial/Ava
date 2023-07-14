import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Index 1 for female voice
engine.setProperty('rate', 150)  # Adjust rate to 150 words per minute
engine.setProperty('volume', 0.7)  # Adjust volume to 70% of maximum
engine.setProperty('pitch', 110)  # Adjust pitch to 110% of default

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

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from string import punctuation
from nltk.stem import WordNetLemmatizer

def summarize_text(text):
    sentences = sent_tokenize(text)

    # Remove stopwords, punctuation, and perform lemmatization
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    clean_sentences = []
    for sentence in sentences:
        words = [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence) if word.isalpha() and word.lower() not in stop_words]
        clean_sentence = ' '.join(words)
        clean_sentences.append(clean_sentence)

    # Check if there are valid sentences left after preprocessing
    if not clean_sentences:
        return ""

    # Calculate word frequency
    word_frequency = FreqDist([word for sentence in clean_sentences for word in nltk.word_tokenize(sentence)])

    # Calculate TF-IDF scores
    tfidf = TfidfVectorizer(preprocessor=lambda x: re.sub(r'\d+', '', x.lower()), token_pattern=r'\b\w+\b', stop_words='english')
    tfidf_scores = tfidf.fit_transform(clean_sentences)

    # Calculate sentence scores based on TF-IDF scores
    sentence_scores = {}
    for i, sentence in enumerate(clean_sentences):
        for word in nltk.word_tokenize(sentence):
            if word in word_frequency.keys() and word in tfidf.vocabulary_:
                if len(sentence.split()) < 30:
                    if i in sentence_scores.keys():
                        sentence_scores[i] += tfidf_scores[i, tfidf.vocabulary_[word]]
                    else:
                        sentence_scores[i] = tfidf_scores[i, tfidf.vocabulary_[word]]

    # Get top 3 sentences with highest scores
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:4]
    summary = [sentences[i] for i in summary_sentences]

    # Rearrange sentences for cohesiveness
    summary_array = tfidf_scores[summary_sentences]
    similarity_matrix = cosine_similarity(summary_array, summary_array)

    rearranged_indices = np.argsort(-similarity_matrix.sum(axis=1))

    rearranged_summary = [summary[i] for i in rearranged_indices]

    # Clean up the summary sentences
    clean_summary = []
    for sentence in rearranged_summary:
        # Remove leading/trailing whitespaces and punctuation
        sentence = sentence.strip(punctuation + " ")
        clean_summary.append(sentence)

    return ' '.join(clean_summary)



def main():
    query = input("Enter your search query (make sure your search query has no miss spellings): ")
    search_results = search_bing(query)
    extracted_results = scrape_results(search_results)

    # Print extracted information
    print("\nExtracted Results:")
    for result in extracted_results:
        print("Title:", result['title'])
        print("URL:", result['url'])
        #print("Snippet:", result['snippet'])
        print()

    # Combine snippets for summarization
    combined_snippets = ' '.join(result['snippet'] for result in extracted_results)

    summary = summarize_text(combined_snippets)
    print("\nSummary:")
    print(summary)
    engine.say(summary)
    engine.runAndWait()

if __name__ == "__main__":
    main()