from core.skill.skill import Skills

class SkillsManager:
    def __init__(self) -> None:
        self.skills = Skills("Data")
        # load skill sample data
        self.training_sentences = []
        self.training_labels = []
        self.labels = []
        self.responses = []

    def get_skills_intent(self):
        for intent, skill in self.skills.skills.items():
            for sample in skill.samples:
                self.training_sentences.append(sample)
                self.training_labels.append(intent)
            if intent not in self.labels:
                self.labels.append(intent)
        return self.training_sentences, self.training_labels

    def get_skills(self):
        for intent, skill in self.skills.skills.items():
            for sample in skill.samples:
                self.training_sentences.append(sample)
                self.training_labels.append(intent)
            if intent not in self.labels:
                self.labels.append(intent)
        return self.labels
