from core.skill.base_skill import BaseSkill
from pathlib import Path
from glob import glob
import os
from importlib.util import spec_from_file_location, module_from_spec


from core.skill.ava_skills.chat import ChatSkill
from core.skill.ava_skills.joke import JokeSkill

skills_list = [
    {
        "name":""
    }
]

class BuiltinSkills():
    def __init__(self):
        self.skills = dict()
        
        # for all subclasses of BaseSkill, instantiate and add them to the skills dict
        for concreteSkill in BaseSkill.__subclasses__():
            skill_instance = concreteSkill()
            self.skills[skill_instance.intent] = skill_instance


if __name__ == '__main__':
    # TESTING
    import jsonpickle
    s = BuiltinSkills()
    # Serialize the object to a JSON string
    json_string = jsonpickle.encode(s)
    print(json_string)
    
    training_sentences = []
    training_labels = []
    labels = []
    responses = []
    
    for intent, skill in s.skills.items():
        for sample in skill.samples:
            training_sentences.append(sample)
            training_labels.append(intent)
        if intent not in labels:
            labels.append(intent)
    
    print("training_sentences:"+str(training_sentences))
    print("training_labels:"+str(training_labels))
    print("labels:"+str(labels))
    print("responses:"+str(responses))

    num_classes = len(labels)
    print(num_classes)

    