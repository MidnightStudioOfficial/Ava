from .utils.referring import ReferencingClassifier
from .response_selector import ResponseMatcher
from .utils.sentiment_analyzer import SentimentAnalyzer
from .model import Model
from os.path import isfile
import logging
from chatterbot2 import ChatBot as CHATBOT
from chatterbot2.trainers import ChatterBotCorpusTrainer
from .chatbot.chatbot import Chatbot


class Conversation():
    """A class representing a conversation between a user and an engine."""

    def __init__(self):
        # Call the __init__ method of the parent class
        super().__init__()

        # Initialize empty lists for utterances, responses, and interactions attributes
        self.utterances = []
        self.responses = []
        self.interactions = []

        # Initialize a ReferencingClassifier object to identify references made by the user during the conversation.
        self.user_refering = ""
        self.bot_emoji = ""

        self.use_gpt = True

        # Initialize and train the ReferencingClassifier to be used for reference identification.
        self.referencingclassifier = ReferencingClassifier()
        self.referencingclassifier.train()

        # Initialize a ResponseMatcher object to select appropriate responses based on user input.
        self.response_matcher = ResponseMatcher()

        self.sentiment_analyzer = SentimentAnalyzer()

        self.model = Model()
        self.gpt_chatbot = Chatbot()

        # Check if the chatbot database exists
        self.chatbot_exists = None
        if isfile("./db.sqlite3") == False:
            logging.debug("chatbot_exists is False")
            self.chatbot_exists = False
        else:
            logging.debug("chatbot_exists is True")
            self.chatbot_exists = True

        # Initialize the chatbot and trainer
        self.chatBot = CHATBOT("Chatbot")
        self.trainer = ChatterBotCorpusTrainer(self.chatBot)

        self.train_bot()

    def train_bot(self) -> None:
        """
        Train the chatbot if it doesn't already exist.
        """
        logging.debug("Training bot")
        if self.chatbot_exists == False:
            self.trainer.train("./Data/training/export.json")
            self.trainer.train("./Data/training/messages.json")

    def get_skill(self, input_text) -> bool:
        """
        Check if the input is a skill.

        Parameters:
            input_text (str): The user input text.

        Returns:
            bool: True if the input is a skill, False otherwise.
        """
        if input_text != "CHAT":
            return True
        else:
            return False

    def interact(self, utterance: str):
        # Predict if the user is referring to the chatbot or not using the ReferencingClassifier.
        self.user_refering = self.referencingclassifier.predict(utterance)

        # If the user refers to the chatbot, update the mood of the chatbot using the SentimentAnalyzer.
        if self.user_refering == "chatbot":
            # Update the mood of the chatbot using the sentiment analyzer
            self.sentiment_analyzer.update_mood(utterance)

            # Get the emoji representation of the chatbot's mood
            self.bot_emoji = self.sentiment_analyzer.mood_as_emoji()

        # Determine the intent of the user's input using the ResponseMatcher.
        virtual_assistant_data = self.response_matcher.determine_intent(utterance)

        # If the intent is unknown, use the Model to make a prediction.
        if virtual_assistant_data["intent"] == 'unknown_intent':
            resalt = self.model.predict(text=utterance)
            is_skill = self.get_skill(resalt["intent"])  # Check if the response is a skill using the get_skill method

            # If it's a skill, return the response.
            if is_skill:
                logging.debug("Skill identified: " + resalt['intent'])
                return resalt['intent'] + str(" " + self.bot_emoji)

            # If not a skill, get a response from the chatbot.
            #bot = self.chatBot.get_response(text=utterance, search_text=utterance)
            bot = self.gpt_chatbot.get_response(utterance)
            return bot + str(" " + self.bot_emoji) #.text
        else:
            # If the intent is known, return the response.
            logging.debug("virtual_assistant_data: " + str(virtual_assistant_data["intent"]))
            return virtual_assistant_data["intent"] + str(" " + self.bot_emoji)

    def get(self):
        """returns all the interactions for the conversation as a list"""
        return self.interactions

    def getConversationLength(self):
        """returns the conversation length"""
        return len(self.interactions)
