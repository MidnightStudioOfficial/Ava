from core.skill.base_skill import BaseSkill
from random import sample


class WeatherSkill(BaseSkill):

    def __init__(self):
        super().__init__()
        self.intent = "ava_skills.weather"
        print(self.intent)
        self.active = True
        self.samples = [
            "tell me the waether",
            "what is the weather",
            "get the weather",
            "give me the weather"
        ]

    def actAndGetResponse(self, **kwargs) -> str:
        return "WEATHER"
