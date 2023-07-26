import spacy
nlp = spacy.load('en_core_web_sm')

def compare(statement_a, statement_b):
        """
        Compare the two input statements.

        :return: The percent of similarity between the closest synset distance.
        :rtype: float
        """
        document_a = nlp(statement_a)
        document_b = nlp(statement_b)

        return document_a.similarity(document_b)

s1 = "google search for" #what are cats
s2 = "search google for that are cats"
while True:
    i = input("you:")
    print(compare(s1, i))