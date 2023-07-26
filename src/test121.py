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

s1 = "google search for what are cats"
s2 = "search google for that are cats"
import spacy
from spacy.matcher import Matcher


# Define keywords for web search trigger
web_search_keywords = ["what", "who", "when", "where", "why", "how"]

# Initialize the Matcher
matcher = Matcher(nlp.vocab)

# Pattern to match questions for web search
web_search_pattern = [{"LOWER": {"IN": web_search_keywords}}]

# Add the pattern to the matcher
matcher.add("WebSearch", [web_search_pattern])

# Function to determine if a query should trigger a web search or get a chatbot response
def process_query(query):
    doc = nlp(query.lower())
    
    # Check if the query matches the web search pattern
    matches = matcher(doc)
    if matches:
        return "WEB_SEARCH"
    
    # If not a web search, use the chatbot to generate a response
    return get_chatbot_response(query)

# Function for the chatbot's response (using spacy as an example)
def get_chatbot_response(query):
    # Replace this with your actual chatbot response generation logic
    response = "Chatbot: I'm sorry, I can't answer that question right now."
    return response
while True:
    # Example usage
    user_input = input("You: ")
    result = process_query(user_input)
    if result == "WEB_SEARCH":
        print("Assistant: Performing a web search for '{}'".format(user_input))
        # Implement the code to perform a Google search here
    else:
        print(result)
