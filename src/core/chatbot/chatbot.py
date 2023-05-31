print('Importing engine (This may take a while!)')
from core.engine.Engine import ConversationalEngine
from core.engine.Conversation import Conversation
from os.path import isfile
import logging
print('Importing chatterbot')
from chatterbot import ChatBot as CHATBOT
from chatterbot.trainers import ChatterBotCorpusTrainer
print('Importing spacy (This may take a while!)')
from spacy import load
print("Importing DONE")

trainingdata='Data/training.csv'
articulationdata='Data/articulations.csv'

logging.basicConfig(level=logging.INFO)

class Chatbot:
    def __init__(self) -> None:
        self.engine = ConversationalEngine(lemmatize_data=True, filepath=trainingdata, modelpath=None)
        self.currentConversation = Conversation(engine=self.engine, articulationdata=articulationdata)
        # Initialize chatbot model here
        self.nlp = load("en_core_web_sm")
        self.chatbot_exists = None
        if isfile("./db.sqlite3") == False:
            logging.debug("chatbot_exists is False")
            self.chatbot_exists = False
        else:
            logging.debug("chatbot_exists is True")
            self.chatbot_exists = True

        self.chatBot = CHATBOT("Chatbot", tagger_language=self.nlp)
        #self.chatBot = ChatBot("Chatbot", tagger_language="en")
        self.trainer = ChatterBotCorpusTrainer(self.chatBot)

    def train_bot(self) -> None:
        logging.debug("Training bot")
        if self.chatbot_exists == False:
         self.trainer.train("./Data/training/export.json")
         self.trainer.train("./Data/training/messages.json")
         #del self.trainer     
    
    def get_skill(self, input):
        if input != "(NOT_FOUND)":
            return True
        else:
            return False
    
    def get_response(self, input):
        payload = self.currentConversation.interact(input, returnPayload=True)
        response = payload.get('articulation')
        is_skill = self.get_skill(response)
        logging.debug(payload.get('probability_matrix'))
        if is_skill == False:
            bot = self.chatBot.get_response(text=input,search_text=input)
            print(bot.text)
            return bot.text
        return response
        
        