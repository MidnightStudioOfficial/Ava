from core.skill.base_skill import BaseSkill
from random import sample


class ChatSkill(BaseSkill):

    def __init__(self):
        super().__init__()
        self.intent = "ava_skills.chat"
        print(self.intent)
        self.active = True
        self.samples = [
            "hello",
            "lets chat",
            "who are you",
            "lets chat",

            "its good that you had fun",

            "hows it going",
            "whats your favorite hobby",
            "what can you do for me",



            "hi",
            "thank you",
            "what is your name",
            "thanks a lot",
            "i admire your creativity",
            "i did not mean to upset you"
        ]

    def actAndGetResponse(self, **kwargs) -> str:
        return "CHAT"
