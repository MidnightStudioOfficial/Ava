t = False
if t == True:
 from chatterbot2.trainers import ListTrainer
 from chatterbot2 import ChatBot

# # create a new chatbot instance
 chatbot = ChatBot('MyChatBot')

# # read the text messages from a file
 with open('messages2.txt', 'r', encoding='utf8') as file:
     messages = file.read().splitlines()
 # train the chatbot using the ListTrainer
 trainer = ListTrainer(chatbot)
 trainer.train(messages)
 trainer.export_for_training('./chat2.json')

# # delete the messages list to free up memory
# del messages

# # add a feature to allow the user to exit the chat
# # while True:
# #     Query = input(">>>")
# #     if Query.lower() == 'exit':
# #         break
# #     bot = chatbot.get_response(text=Query, search_text=Query)
# #     print(bot)

# #     # add a feature to allow the user to provide feedback on the chatbot's response
# #     feedback = input("Was this response helpful? (yes/no) ")
# #     if feedback.lower() == 'no':
# #         correction = input("What would have been a better response? ")
# #         trainer.train([Query, correction])

# print("Goodbye!")


from chatterbot2.exceptions import OptionalDependencyImportError
import io
import tqdm
import os
CORPUS_EXTENSION = 'yml'
def read_corpus(file_name):
    """
    Read and return the data from a corpus json file.
    """
    try:
        import yaml
    except ImportError:
        message = (
            'Unable to import "yaml".\n'
            'Please install "pyyaml" to enable chatterbot corpus functionality:\n'
            'pip3 install pyyaml'
        )
        raise OptionalDependencyImportError(message)

    with io.open(file_name, encoding='utf-8') as data_file:
        return yaml.safe_load(data_file)
def load_corpus(*data_file_paths):
    """
    Return the data contained within a specified corpus.
    """
    for file_path in data_file_paths:
        corpus = []
        corpus_data = read_corpus(file_path)

        conversations = corpus_data.get('conversations', [])
        corpus.extend(conversations)

        categories = corpus_data.get('categories', [])
        print(f"corpus:{corpus} categories:{categories} file_path:{file_path}")
        yield corpus, categories, file_path
        
data_file_paths = ["./chat2.json"]
for corpus, categories, file_path in load_corpus(*data_file_paths):

            statements_to_create = []

            # Train the chat bot with each statement and response pair
            prog = tqdm.tqdm(enumerate(corpus))
            for conversation_count, conversation in prog:

                
                prog.set_description_str("{} {} {} {:.3}%".format('Training ' + str(os.path.basename(file_path)),
                        conversation_count + 1,
                        len(corpus), (conversation_count + 1) * 100.0 / len(corpus)))

                previous_statement_text = None
                previous_statement_search_text = ''

                for text in conversation:
                    print("text:"+str(text))
