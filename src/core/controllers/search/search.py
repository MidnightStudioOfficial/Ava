import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from string import punctuation
from nltk.stem import WordNetLemmatizer

class TextSummarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def search_bing(self, query):
        url = f"https://www.bing.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='b_algo')
        return results

    def scrape_results(self, results):
        extracted_results = []
        for result in results:
            title = result.find('h2').get_text()
            url = result.find('a')['href']
            snippet = result.find('p').get_text()

            # Remove unwanted phrases like "WebJul 3, 2023"
            snippet = re.sub(r'(Web|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}', '', snippet)

            extracted_results.append({'title': title, 'url': url, 'snippet': snippet})
        return extracted_results

    def determine_summary_length(self, sentences, tfidf_scores):
        sentence_scores = tfidf_scores.sum(axis=1)
        avg_score = sentence_scores.mean()
        threshold = avg_score * 0.8  # Set the threshold to 80% of the average score

        summary_sentences = []
        for i, score in enumerate(sentence_scores):
            if score >= threshold:
                summary_sentences.append(i)

        desired_length = min(4, len(summary_sentences))  # Set the desired length to 4 or the number of sentences above the threshold, whichever is smaller
        return desired_length

    def determine_summary_length2(self, sentences, tfidf_scores, similarity_matrix):
        sentence_scores = tfidf_scores.sum(axis=1)
        sorted_indices = np.argsort(-sentence_scores)  # Sort sentence indices by score in descending order

        summary_sentences = []
        used_indices = set()
        for index in sorted_indices:
            if index.item() not in used_indices:  # Convert index to item() to access the actual value
                summary_sentences.append(index.item())  # Convert index to item() to access the actual value
                used_indices.add(index.item())  # Convert index to item() to access the actual value
                # Consider similar sentences to maintain cohesiveness in the summary
                for i, similarity in enumerate(similarity_matrix[index.item()]):  # Convert index to item() to access the actual value
                    if similarity >= 0.2:  # Set a similarity threshold of 0.2 (adjust as needed)
                        used_indices.add(i)

            if len(summary_sentences) >= 4:
                break

        desired_length = min(4, len(summary_sentences))  # Set the desired length to 4 or the number of selected sentences, whichever is smaller
        return desired_length


    def determine_summary_length3(self, sentences, tfidf_scores, similarity_matrix):
        sentence_scores = tfidf_scores.sum(axis=1)
        sorted_indices = np.argsort(-sentence_scores)  # Sort sentence indices by score in descending order

        summary_sentences = []
        used_indices = set()
        for index in sorted_indices:
            if index.item() not in used_indices:  # Convert index to item() to access the actual value
                summary_sentences.append(index.item())  # Convert index to item() to access the actual value
                used_indices.add(index.item())  # Convert index to item() to access the actual value
                # Consider similar sentences to maintain cohesiveness in the summary
                for i, similarity in enumerate(similarity_matrix[index.item()]):  # Convert index to item() to access the actual value
                    if similarity >= 0.2:  # Set a similarity threshold of 0.2 (adjust as needed)
                        used_indices.add(i)

                if len(summary_sentences) >= len(sentences) * 0.5:  # Include up to 50% of the sentences in the summary
                    break

        desired_length = min(4, len(summary_sentences))  # Set the desired length to 4 or the number of selected sentences, whichever is smaller
        return desired_length

    def determine_summary_length4(self, sentences, tfidf_scores, similarity_matrix):
        sentence_scores = tfidf_scores.sum(axis=1)
        sorted_indices = np.argsort(-sentence_scores)  # Sort sentence indices by score in descending order

        summary_sentences = []
        used_indices = set()
        max_sentences = min(4, len(sentences))  # Set the maximum number of sentences to include in the summary

        for index in sorted_indices:
            if len(summary_sentences) >= max_sentences:
                break

            if index.item() not in used_indices:
                summary_sentences.append(index.item())
                used_indices.add(index.item())

                for i, similarity in enumerate(similarity_matrix[index.item()]):
                    if similarity >= 0.2 and i not in used_indices:  # Adjust the similarity threshold as needed
                        summary_sentences.append(i)
                        used_indices.add(i)

        desired_length = min(max_sentences, len(summary_sentences))
        return desired_length

    def preprocess_text(self, text):
        clean_sentences = []
        sentences = sent_tokenize(text)
        for sentence in sentences:
            words = [self.lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(sentence) if word.isalpha() and word.lower() not in self.stop_words]
            clean_sentence = ' '.join(words)
            clean_sentences.append(clean_sentence)
        return clean_sentences

    def summarize_text(self, text):
        clean_sentences = self.preprocess_text(text)

        if not clean_sentences:
            return ""

        word_frequency = FreqDist([word for sentence in clean_sentences for word in nltk.word_tokenize(sentence)])

        tfidf = TfidfVectorizer(preprocessor=lambda x: re.sub(r'\d+', '', x.lower()), token_pattern=r'\b\w+\b', stop_words='english')
        tfidf_scores = tfidf.fit_transform(clean_sentences)

        sentence_scores = {}
        for i, sentence in enumerate(clean_sentences):
            for word in nltk.word_tokenize(sentence):
                if word in word_frequency.keys() and word in tfidf.vocabulary_:
                    if len(sentence.split()) < 30:
                        if i in sentence_scores.keys():
                            sentence_scores[i] += tfidf_scores[i, tfidf.vocabulary_[word]]
                        else:
                            sentence_scores[i] = tfidf_scores[i, tfidf.vocabulary_[word]]

        desired_length = min(4, len(clean_sentences))
        #desired_length = determine_summary_length(sentences, tfidf_scores)
        #desired_length = determine_summary_length2(sentences, tfidf_scores, cosine_similarity(tfidf_scores, tfidf_scores))
        #desired_length = determine_summary_length3(sentences, tfidf_scores, cosine_similarity(tfidf_scores, tfidf_scores))
        #desired_length = determine_summary_length4(sentences, tfidf_scores, cosine_similarity(tfidf_scores, tfidf_scores))

        summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:desired_length]
        summary = [clean_sentences[i] for i in summary_sentences]

        summary_array = tfidf_scores[summary_sentences]
        similarity_matrix = cosine_similarity(summary_array, summary_array)

        rearranged_indices = np.argsort(-similarity_matrix.sum(axis=1))

        rearranged_summary = [summary[i] for i in rearranged_indices]

        clean_summary = []
        for sentence in rearranged_summary:
            sentence = sentence.strip(punctuation + " ")
            clean_summary.append(sentence)

        return ' '.join(clean_summary)

    def run_summarization_TEST(self):
        query = input("Enter your search query (Make sure your search query has no misspellings): ")
        search_results = self.search_bing(query)
        extracted_results = self.scrape_results(search_results)

        print("\nExtracted Results:")
        for result in extracted_results:
            print("Title:", result['title'])
            print("URL:", result['url'])
            print()

        combined_snippets = ' '.join(result['snippet'] for result in extracted_results)

        summary = self.summarize_text(combined_snippets)
        print("\nSummary:")
        print(summary)


if __name__ == "__main__":
    summarizer = TextSummarizer()
    summarizer.run_summarization_TEST()
