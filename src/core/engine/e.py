from Engine2 import ConversationalEngine
from Conversation import Conversation

trainingdata='training.csv'
articulationdata='articulations.csv'

engine = ConversationalEngine(lemmatize_data=True, filepath=trainingdata, modelpath=None)
currentConversation = Conversation(engine=engine, articulationdata=articulationdata)
user = input("enter text")
payload = currentConversation.interact(user, returnPayload=True)
response = payload.get('articulation')
print(payload.get('probability'))
print(payload.get('probability_matrix'))
print(response)