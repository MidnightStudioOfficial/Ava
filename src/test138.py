import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
import random

nltk.download('punkt')

def paraphrase_sentence(input_sentence, num_paraphrases=5):
    # Sample paraphrases will be stored here
    paraphrases = []
    
    # Tokenize the input sentence
    input_tokens = word_tokenize(input_sentence)
    input_text = " ".join(input_tokens)
    
    # Create the TfidfVectorizer
    vectorizer = TfidfVectorizer()
    
    # Calculate the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform([input_text])
    
    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get the TF-IDF scores for the input sentence
    tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
    
    # Sort words based on their TF-IDF scores in descending order
    sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Generate paraphrases by replacing high-TF-IDF words with synonyms
    for _ in range(num_paraphrases):
        paraphrase_tokens = input_tokens.copy()
        
        # Randomly select a word with a high TF-IDF score to replace
        word_to_replace = random.choice(sorted_words[:int(len(sorted_words) * 0.3)])[0]
        
        # Get synonyms for the selected word
        synonyms = set()
        for synset in nltk.corpus.wordnet.synsets(word_to_replace):
            for lemma in synset.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
        
        # If synonyms exist, replace the word in the paraphrased version
        if synonyms:
            new_word = random.choice(list(synonyms))
            paraphrase_tokens = [new_word if word == word_to_replace else word for word in paraphrase_tokens]
        
        # Add the paraphrased sentence to the list
        paraphrases.append(" ".join(paraphrase_tokens))
    
    return paraphrases

if __name__ == "__main__":
    input_sentence = "The quick brown fox jumps over the lazy dog."
    num_paraphrases = 5
    
    paraphrases = paraphrase_sentence(input_sentence, num_paraphrases)
    
    print("Original Sentence: ", input_sentence)
    print("\nParaphrases:")
    for idx, paraphrase in enumerate(paraphrases, 1):
        print(f"{idx}. {paraphrase}")
