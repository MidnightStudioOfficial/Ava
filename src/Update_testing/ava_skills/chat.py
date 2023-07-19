from base_skill import BaseSkill
from random import sample


class ChatSkill(BaseSkill):

    def __init__(self):
        super().__init__()
        self.intent = __name__
        self.active = True
        self.samples = [
            "hello",
            "lets chat",
            "who are you",
            "lets chat",
            
            "its good that you had fun"
        ]

    def actAndGetResponse(self, **kwargs) -> str:
        return "CHAT"