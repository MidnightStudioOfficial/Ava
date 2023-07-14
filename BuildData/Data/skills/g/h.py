import time
from core.skill.base_skill import BaseSkill
from random import sample


class DateSkill(BaseSkill):

    def __init__(self):
        super().__init__()
        self.intent = __name__
        self.active = True
        self.samples = [
            "date",
            "get date",
            "what date is it",
            "what is the date",
            "what date is it now",
            "what date is it today"
        ]
        self.responses = [
            "The date is $0",
            "Today is $0"
        ]

    def actAndGetResponse(self, **kwargs) -> str:
        response = sample(self.responses, 1)[0]    
        today = time.strftime("%d %B, %Y")
        return response.replace("$0", today)
