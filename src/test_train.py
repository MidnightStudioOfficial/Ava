from chatterbot2.trainers import ListTrainer
from chatterbot2 import ChatBot

# create a new chatbot instance
chatbot = ChatBot('MyChatBot')

# read the text messages from a file
with open('messages.txt', 'r', encoding='utf8') as file:
    messages = file.read().splitlines()

# train the chatbot using the ListTrainer
trainer = ListTrainer(chatbot)
trainer.train(messages)
trainer.export_for_training('./chat.json')

# delete the messages list to free up memory
del messages

# add a feature to allow the user to exit the chat
while True:
    Query = input(">>>")
    if Query.lower() == 'exit':
        break
    bot = chatbot.get_response(text=Query, search_text=Query)
    print(bot)

    # add a feature to allow the user to provide feedback on the chatbot's response
    feedback = input("Was this response helpful? (yes/no) ")
    if feedback.lower() == 'no':
        correction = input("What would have been a better response? ")
        trainer.train([Query, correction])

print("Goodbye!")