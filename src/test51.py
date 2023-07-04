from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation


class Comparator:
    def __init__(self):
        pass
    
    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare(self, statement_a, statement_b):
        return 0


class LevenshteinDistance(Comparator):
    def compare(self, statement_a, statement_b):
        if not statement_a or not statement_b:
            return 0

        statement_a_text = str(statement_a.lower())
        statement_b_text = str(statement_b.lower())

        similarity = SequenceMatcher(None, statement_a_text, statement_b_text)
        percent = round(similarity.ratio(), 2)

        return percent

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.metrics.pairwise import cosine_similarity
# from difflib import SequenceMatcher


# class TopicAndCosineSimilarity(Comparator):
#     def compare(self, statement_a, statement_b):
#         if not statement_a or not statement_b:
#             return 0

#         statement_a_text = str(statement_a)
#         statement_b_text = str(statement_b)

#         corpus = [statement_a_text, statement_b_text]

#         vectorizer = TfidfVectorizer()
#         tfidf_matrix = vectorizer.fit_transform(corpus)

#         lda = LatentDirichletAllocation(n_components=5, random_state=42)
#         topic_matrix = lda.fit_transform(tfidf_matrix)

#         topic_similarities = cosine_similarity(topic_matrix[0].reshape(1, -1), topic_matrix[1].reshape(1, -1))
#         topic_similarity_percent = round(topic_similarities[0][0] * 100, 2)

#         cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
#         cosine_similarity_percent = round(cosine_similarities[0][0] * 100, 2)

#         # Combine the similarity scores using a weighted average or any other method
#         # For example, you can assign higher weightage to topic similarity
#         combined_similarity_percent = (0.7 * topic_similarity_percent) + (0.3 * cosine_similarity_percent)

#         return combined_similarity_percent


class TopicAndCosineSimilarity(Comparator):
    def compare(self, statement_a, statement_b):
        if not statement_a or not statement_b:
            return 0

        statement_a_text = str(statement_a)
        statement_b_text = str(statement_b)

        corpus = [statement_a_text, statement_b_text]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        topic_matrix = lda.fit_transform(tfidf_matrix)

        topic_similarities = cosine_similarity(topic_matrix[0].reshape(1, -1), topic_matrix[1].reshape(1, -1))
        topic_similarity_percent = round(topic_similarities[0][0] * 100, 2)

        cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        cosine_similarity_percent = round(cosine_similarities[0][0] * 100, 2)

        # Combine the similarity scores using a weighted average or any other method
        # For example, you can assign higher weightage to topic similarity
        combined_similarity_percent = (0.7 * topic_similarity_percent) + (0.3 * cosine_similarity_percent)

        return combined_similarity_percent

class NgramSimilarity(Comparator):
    def __init__(self, n=3):
        super().__init__()
        self.n = n

    def compare(self, statement_a, statement_b):
        if not statement_a or not statement_b:
            return 0

        statement_a_ngrams = self._generate_ngrams(statement_a.lower(), self.n)
        statement_b_ngrams = self._generate_ngrams(statement_b.lower(), self.n)

        intersection = len(set(statement_a_ngrams).intersection(set(statement_b_ngrams)))
        union = len(set(statement_a_ngrams).union(set(statement_b_ngrams)))

        if union == 0:
            return 0

        similarity = intersection / union
        #percent = round(similarity * 100, 2)
        percent = similarity * 100

        return percent

    def _generate_ngrams(self, text, n):
        return [text[i:i + n] for i in range(len(text) - n + 1)]

class CosineSimilarity(Comparator):
    def compare(self, statement_a, statement_b):
        if not statement_a or not statement_b:
            return 0

        statement_a_text = str(statement_a)
        statement_b_text = str(statement_b)

        corpus = [statement_a_text, statement_b_text]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        cosine_similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        percent = round(cosine_similarities[0][0] * 100, 2)

        return percent

class TopicModeling(Comparator):
    def compare(self, statement_a, statement_b):
        if not statement_a or not statement_b:
            return 0

        statement_a_text = str(statement_a)
        statement_b_text = str(statement_b)

        corpus = [statement_a_text, statement_b_text]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)

        lda = LatentDirichletAllocation(n_components=5, random_state=42)
        topic_matrix = lda.fit_transform(tfidf_matrix)

        # Calculate the cosine similarity between topic distributions
        topic_similarities = cosine_similarity(topic_matrix[0].reshape(1, -1), topic_matrix[1].reshape(1, -1))
        percent = round(topic_similarities[0][0] * 100, 2)

        return percent
    
class avrig(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, statement_a, statement_b):
        """
        Compare the two input statements.

        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """

        # Return 0 if either statement has a falsy text value
        if not statement_a or not statement_b:
            return 0
        
        s1 = CosineSimilarity()
        s1_r = s1.compare(statement_a,statement_b)
        
        s2 = TopicModeling()
        s2_r = s2.compare(statement_a,statement_b)

        percent = (s1_r + s2_r) / 2

        return percent

c1 = "That is nice to hear."
c2 = "That is not nice to hear."

g1 = TopicModeling()
print("TopicModeling:"+str(g1.compare(c1, c2)))
g2 = TopicAndCosineSimilarity()
print("TopicAndCosineSimilarity:"+str(g2.compare(c1, c2)))
g3 = CosineSimilarity()
print("CosineSimilarity:"+str(g3.compare(c1, c2)))
g5 = LevenshteinDistance()
print("LevenshteinDistance:"+str(g5.compare(c1, c2)))
g4 = avrig()
print(g4.compare(c1, c2))