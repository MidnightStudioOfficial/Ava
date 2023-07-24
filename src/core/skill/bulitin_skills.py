"""
Built-in Skills Module

This module defines a class to manage built-in skills for an AI assistant application. It imports specific skills from their respective modules and instantiates them, creating instances of each skill class. The instantiated skills are stored in a dictionary, allowing easy access and management of the skills by using their intents as keys.

The `BuiltinSkills` class is responsible for the following tasks:
1. Importing specific skills from their respective modules.
2. Instantiating each skill class derived from the `BaseSkill` class.
3. Storing the instantiated skills in the `self.skills` dictionary with the skill intent as the key.

The `skills_list` variable is not directly used within this class, but it could be used to store additional information about each skill, such as their name, description, or other relevant data, if needed elsewhere in the application.

Please note that the `BaseSkill` class and its subclasses are expected to be defined in the appropriate modules before using this module.
"""
from core.skill.base_skill import BaseSkill

# Import specific skills from their respective modules
from core.skill.ava_skills.chat import ChatSkill
from core.skill.ava_skills.joke import JokeSkill
from core.skill.ava_skills.weather import WeatherSkill
from core.skill.ava_skills.music import MusicSkill

skills_list = [
    {
        "name":""
    }
]

class BuiltinSkills():
    def __init__(self):
        # Create an empty dictionary to store skills with their intents as keys
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
