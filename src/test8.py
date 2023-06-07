import concurrent.futures
from os.path import isfile
import logging
import json

def import_modules(module_name):
    if module_name == 'engine':
        print('Importing engine (This may take a while!)')
        from core.engine.Engine import ConversationalEngine
        from core.engine.Conversation import Conversation
    elif module_name == 'brain':
        print("Importing brain (This may take a while!)")
        from core.brain.brain import Brain
    elif module_name == 'chatterbot':
        print('Importing chatterbot')
        from chatterbot import ChatBot as CHATBOT
        from chatterbot.trainers import ChatterBotCorpusTrainer
    elif module_name == 'spacy':
        print('Importing spacy (This may take a while!)')
        from spacy import load

with concurrent.futures.ThreadPoolExecutor() as executor:
    modules = ['engine', 'brain', 'chatterbot', 'spacy']
    results = [executor.submit(import_modules, module) for module in modules]

print("Importing DONE")
