from .utils.referring import ReferencingClassifier

# Define a Conversation class that represents a conversation between a user and an engine
class Conversation():
    def __init__(self):
        # Call the __init__ method of the parent class
        super().__init__()

        # Initialize empty lists for utterances, responses, and interactions attributes
        self.utterances = []
        self.responses = []
        self.interactions = []
        self.user_refering = ""

        # Initialize a ReferencingClassifier object and train it
        self.referencingclassifier = ReferencingClassifier()
        self.referencingclassifier.train()

    def interact(self, utterance: str):
        self.user_refering = self.referencingclassifier.predict(utterance)

    def get(self):
        """returns all the interactions for the conversation as a list"""
        return self.interactions

    def getConversationLength(self):
        """returns the conversation length"""
        return len(self.interactions)
