import objgraph
import gc
import time
from pympler.tracker import SummaryTracker
tracker = SummaryTracker()
from core.chatbot.chatbot import Chatbot, ChatbotProfile

trainingdata='Data/training.csv'
chatbot = Chatbot()
chatbot.train_bot()
thresholds = gc.get_threshold()
print(thresholds)
thresholds2 = gc.get_count()
print(thresholds2)
# tracker.print_diff()
# #engine = ConversationalEngine(lemmatize_data=True, filepath=trainingdata, modelpath=None)
# objgraph.show_refs(chatbot, max_depth=6, filename='sample-graph.png')

# Importing gc module

while True:
    time.sleep(6)
    i = input('ENTER:')
    print(chatbot.get_response(i))
    thresholds2 = gc.get_count()
    print(thresholds2)
    collected = gc.collect()
    print("Garbage collector: collected",
          "%d objects." % collected)
    thresholds = gc.get_threshold()
    print(thresholds)
    thresholds2 = gc.get_count()
    print(thresholds2)
