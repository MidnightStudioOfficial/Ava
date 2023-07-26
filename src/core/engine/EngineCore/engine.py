from .utils.preprocessing import TextPreprocessor
from .model import Model

class MainEngine:
    def __init__(self) -> None:
        self.model = Model()

    def getIntent(self, input_text: str):
        return self.model.predict(text=input_text)