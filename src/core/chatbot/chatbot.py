print('Importing engine (This may take a while!)')
from core.engine.Engine import ConversationalEngine
from core.engine.Conversation import Conversation
print("Importing brain (This may take a while!)")
from core.brain.brain import Brain
from os.path import isfile
import logging
import json
print('Importing chatterbot')
from chatterbot2 import ChatBot as CHATBOT
from chatterbot2.trainers import ChatterBotCorpusTrainer
print("Importing DONE")

Debug = False

if Debug != True:
 trainingdata='Data/training.csv'
 articulationdata='Data/articulations.csv'
else:
 trainingdata='Data/training_dev.csv'
 articulationdata='Data/articulations_dev.csv'

logging.basicConfig(level=logging.INFO)

brain = Brain()

class ChatbotProfile:
      def __init__(self) -> None:
          self.profile_data = {
              "name": None,
              "gender": None,
              "brain": {
                   "traits": [],
                   "mood": None,
                   "thought": None,
                   "memory": {}
              }

          }
          brain.start()
          
      def update_profile(self): #, key, value
          self.profile_data["brain"]["mood"] = brain.mood
          self.profile_data["brain"]["thought"] = brain.thought
      
      def _set_profile_data(self):
          brain.mood = self.profile_data["brain"]["mood"]
          brain.thought = self.profile_data["brain"]["thought"]
      
      def load_profile(self):
        # Open the JSON file
        try:
         with open('./Data/chatbot/profile.json', 'r') as f:
             # Load the contents of the file as a Python object
             data = json.load(f)
             self.profile_data["name"] = data["name"]
             self.profile_data["gender"] = data["gender"]
             self.profile_data["brain"]["traits"] = data["brain"]["traits"]
             self.profile_data["brain"]["mood"] = data["brain"]["mood"]
             self.profile_data["brain"]["thought"] = data["brain"]["thought"]
             self.profile_data["brain"]["memory"] = data["brain"]["memory"]
        except FileNotFoundError:
           print("File not found")
        except json.JSONDecodeError:
           print("Invalid JSON syntax")
        self._set_profile_data()
      
      def save_profile(self):
       self.update_profile()
       try:
         with open('./Data/chatbot/profile.json', 'w') as f:
             # Load the contents of the file as a Python object
             data = json.dump(self.profile_data, f)
       except FileNotFoundError:
           print("File not found")
       except json.JSONDecodeError:
           print("Invalid JSON syntax")

class Chatbot:
    def __init__(self, splash_screen) -> None:
        # Initialize the conversational engine and conversation
        splash_screen.set_text("Initializing the conversational engine and conversation")
        self.engine = ConversationalEngine(lemmatize_data=True, filepath=trainingdata, modelpath=None)
        self.currentConversation = Conversation(engine=self.engine, articulationdata=articulationdata)

        # Check if the chatbot database exists
        self.chatbot_exists = None
        if isfile("./db.sqlite3") == False:
            logging.debug("chatbot_exists is False")
            self.chatbot_exists = False
        else:
            logging.debug("chatbot_exists is True")
            self.chatbot_exists = True

        # Initialize the chatbot and trainer
        splash_screen.set_text("Initializing the chatbot and trainer")
        self.chatBot = CHATBOT("Chatbot") #, tagger_language=self.nlp
        self.trainer = ChatterBotCorpusTrainer(self.chatBot)

    def train_bot(self) -> None:
        """
        Train the chatbot if it doesn't already exist.
        """
        logging.debug("Training bot")
        if self.chatbot_exists == False:
            self.trainer.train("./Data/training/export.json")
            self.trainer.train("./Data/training/messages.json")

    def get_skill(self, input):
        # Check if the input is a skill
        if input != "(NOT_FOUND)":
            return True
        else:
            return False

    def get_response(self, input):
        # Get a response from the conversational engine or chatbot
        payload = self.currentConversation.interact(input, returnPayload=True)
        response = payload.get('articulation')
        is_skill = self.get_skill(response)
        print(payload.get('probability_matrix'))
        if is_skill == False:
            bot = self.chatBot.get_response(text=input, search_text=input)
            print(bot.text)
            return bot.text
        return response
