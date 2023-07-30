import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_", " ").lower())
    return list(synonyms)

def rewrite_sentence_with_synonyms(sentence):
    # Tokenize the input sentence
    tokens = word_tokenize(sentence.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = tokens # [word for word in tokens if word.isalpha() and word not in stop_words]

    # Generate synonyms for each token
    synonyms_dict = {}
    for token in filtered_tokens:
        synonyms = get_synonyms(token)
        if synonyms:
            synonyms_dict[token] = synonyms

    # Replace words with most similar synonyms using TF-IDF and cosine similarity
    rewritten_sentences = []
    for idx in range(len(filtered_tokens)):
        token = filtered_tokens[idx]
        if token in synonyms_dict:
            synonyms = synonyms_dict[token]
            synonyms.append(token)  # Include the original word in synonyms for comparison
            synonyms_str = " ".join(synonyms)
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform([synonyms_str, " ".join(filtered_tokens)])
            similarity_score = cosine_similarity(tfidf_matrix)
            most_similar_word = synonyms[similarity_score[0].argmax()]
            temp_tokens = filtered_tokens.copy()
            temp_tokens[idx] = most_similar_word
            rewritten_sentence = ' '.join(temp_tokens)
            rewritten_sentences.append(rewritten_sentence)

    return rewritten_sentences

if __name__ == "__main__":
    input_sentence = "The quick brown fox jumps over the lazy dog"
    rewritten_sentences = rewrite_sentence_with_synonyms(input_sentence)
    if rewritten_sentences:
        print("Original Sentence:")
        print(input_sentence)
        print("\nRewritten Sentences with Most Similar Synonyms:")
        for sentence in rewritten_sentences:
            print(sentence)
    else:
        print("No synonyms found for any word in the sentence.")
