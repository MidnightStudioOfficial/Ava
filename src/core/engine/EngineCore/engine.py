from .conversation import Conversation
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("tensorflow").disabled = True


class MainEngine:
    def __init__(self) -> None:
        self.conversation = Conversation()

    def getIntent(self, input_text: str):
        return self.conversation.interact(input_text)
