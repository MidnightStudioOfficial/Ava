from chatterbot2 import ChatBot
from chatterbot2.trainers import ChatterBotCorpusTrainer

chatBot = ChatBot("Chatbot")
trainer = ChatterBotCorpusTrainer(chatBot)


trainer.train("./english")
#trainer.train("export.json")
trainer.export_for_training('./export.json')