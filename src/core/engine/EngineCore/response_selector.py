from .data_helpers.web_scrap import WebScrap
from .data_helpers.wikipedia_scrap import WikipediaScrap


class ResponseMatcher:
    def __init__(self) -> None:
        """
        ResponseMatcher class for intent determination based on different modules.

        Each module provides a specific functionality for intent determination.

        Attributes:
            modules (dict): A dictionary containing module instances with unique keys.

        Example usage:
            response_matcher = ResponseMatcher()
            intent_result = response_matcher.determine_intent(input_text)
        """
        self.modules = {
            'web_scrap': WebScrap(),
            'wikipedia_scrap': WikipediaScrap()
        }

    def determine_intent(self, input_text: str) -> dict:
        """
        Determine the intent of the input text using different modules.

        The method iterates through the available modules and processes the input
        text using each module to find a matching intent.

        Args:
            input_text (str): The input text for which the intent needs to be determined.

        Returns:
            dict: A dictionary containing the intent and its probability.
        """
        for _, module_instance in self.modules.items():
            result = module_instance.process(input_text)
            if result != "none":
                return {
                    'intent': result,
                    'probability': 1
                }

        # If no matching intent is found, return an unknown intent
        return {
            'intent': 'unknown_intent',
            'probability': 0
        }
