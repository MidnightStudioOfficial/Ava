from core.engine.Engine import ConversationalEngine
from core.engine.Conversation import Conversation

trainingdata='Data/training.csv'
articulationdata='Data/articulations.csv'

engine = ConversationalEngine(lemmatize_data=True, filepath=trainingdata, modelpath=None)
currentConversation = Conversation(engine=engine, articulationdata=articulationdata)
user = input("enter text")
payload = currentConversation.interact(user, returnPayload=True)
response = payload.get('articulation')
print(payload.get('probability'))
print(payload.get('probability_matrix'))
print(response)
