import wikipedia
import re


class WikipediaScrap:
    def __init__(self) -> None:
        pass

    def check_if_requested(self, text: str):
        """
        Checks if a Wikipedia search request is present in the given text.

        Args:
            text (str): The input text to check for search requests.

        Returns:
            str: The search request if found, otherwise returns "none".
        """
        # Define the regular expression pattern
        pattern = r'(?:wikipedia\s+search|search\s+wikipedia)\s+for\s+(.+)'

        # Use re.search() to find the pattern in the text
        match = re.search(pattern, text, re.IGNORECASE)

        # If a match is found, return the search request, otherwise return None
        return match.group(1) if match else "none"

    def process(self, input_text: str):
        """
        Processes the input text, searches Wikipedia for the specified query,
        extracts search results, and provides a summary of the results.

        Args:
            input_text (str): The input text containing the Wikipedia search request.

        Returns:
            str: The summary of the search results, or "none" if no search request is found.
        """
        search_request = self.check_if_requested(input_text)

        # If a search request is found, search Wikipedia for the specified query
        if search_request != "none":
            # Search Wikipedia for the specified query
            try:
                article = wikipedia.summary(search_request, sentences=5)
                return article
            except wikipedia.exceptions.PageError:
                # If the Wikipedia page is not found, inform the user and return "none".
                print("Sorry, I couldn't find a Wikipedia article for that.")
                return "Sorry, I couldn't find a Wikipedia article for that."

        # If no search request is found, return "none"
        return "none"
