from core.skill.base_skill import BaseSkill
from random import sample


class MusicSkill(BaseSkill):

    def __init__(self):
        super().__init__()
        self.intent = "ava_skills.music"
        print(self.intent)
        self.active = True
        self.samples = [
            "could you please play some music",
            "play music"
        ]

    def actAndGetResponse(self, **kwargs) -> str:
        return "MUSIC"
