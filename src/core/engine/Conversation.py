#from core.engine.Engine import ConversationalEngine
from core.engine.ArticulationMapper import ArticulationMapper

# Import the namedtuple class from the collections module
from collections import namedtuple

# Define a Conversation class that represents a conversation between a user and an engine
class Conversation():
    def __init__(self, engine, articulationdata: str): #: ConversationalEngine
        """
        arguments:
        app -- any object type, for reference by the conversation
        engine -- ConversationalEngine | an instantiated conversational engine
        articulationdata -- str | filepath to the articulation .csv file
        """
        # Call the __init__ method of the parent class
        super().__init__()

        # Set the engine attribute to the engine argument
        self.engine = engine

        # Initialize empty lists for utterances, responses, and interactions attributes
        self.utterances = []
        self.responses = []
        self.interactions = []

        # Create an ArticulationMapper object with the articulationdata argument and set it to the articMapper attribute
        self.articMapper = ArticulationMapper(articulationdata)

    # Define an interact method that takes an utterance argument and an optional returnPayload argument
    def interact(self, utterance: str, returnPayload = False):
        """
        Processes an utterance from the user and returns a response.

        arguments:
        utterance -- str | the input utterance from the user
        returnPayload -- bool | True if desired return value is conversation payload, False if desired return value is just articulation string. Default is False.

        returns: 
            str articulation value if returnPayload arg is False, otherwise:
            dictionary with key-value pairs of:
            articulation -- str  | the articulation for the matched intent
            intent -- str | the matched intent
            probability -- float | the probability associated with the matched intent
            probability_matrix -- list | a 2-dimensional list with elements of [intent name, probability] for all intents in the training set, sorted by highest to lowest probability
        """
        # Append the utterance argument to the utterances attribute list
        self.utterances.append(utterance)

        # Get a response from the engine using its getIntent method with the utterance argument and set it to a response variable
        response = self.engine.getIntent(utterance)

        # Append the intent value from the response dictionary to the responses attribute list
        self.responses.append(response.get('intent'))

        # Check if the probability value in the response dictionary is greater than 0.3
        if response.get('probability') > 0.3:
            # Get an articulation from the articMapper object using its get method with the intent value from the response dictionary and set it to an articulation variable
            articulation = self.articMapper.get(response.get('intent'))

            # Check if articulation is None
            if articulation == None:
                # Get an articulation for 'no_articulation' from the articMapper object using its get method and set it to an articulation variable
                articulation = self.articMapper.get('no_articulation')

         # If probability value in response dictionary is not greater than 0.3
        else:
            # Get an articulation for 'default' from the articMapper object using its get method and set it to an articulation variable
            articulation = self.articMapper.get('default')
        # Create a namedtuple called Interaction with 'utterance' and 'response' fields
        Interaction = namedtuple('Interaction', ['utterance', 'response'])

        # Append a new Interaction object with utterance and articulation arguments to interactions attribute list
        self.interactions.append(Interaction(utterance, articulation))
        if returnPayload == False:
            return articulation
        else:
            return {
                'articulation' : articulation,
                'intent' : response.get('intent'),
                'probability' : response.get('probability'),
                'probability_matrix' : response.get('probability_matrix')
            }

    def get(self):
        """returns all the interactions for the conversation as a list"""
        return self.interactions

    def getConversationLength(self):
        """returns the conversation length"""
        return len(self.interactions)
