from base_skill import BaseSkill
from pathlib import Path
from glob import glob
import os
from importlib.util import spec_from_file_location, module_from_spec


from ava_skills.chat import ChatSkill
from ava_skills.joke import JokeSkill

skills_list = [
    {
        "name":""
    }
]

class Skills():


    def __init__(self):
        self.skills = dict()
        # path = Path(__file__).parent.resolve()
        # modules = glob(str(path) + "/skills/*.py", recursive = True)
        # for m in modules:
        #     module_name = os.path.split(m)[-1].strip(".py")
        #     imported_module = self.dynamic_import(module_name, m)
        #     # globals()[module_name] = imported_module
        #     # self.skills[module_name] = imported_module
        
        # for all subclasses of BaseSkill, instantiate and add them to the skills dict
        for concreteSkill in BaseSkill.__subclasses__():
            skill_instance = concreteSkill()
            self.skills[skill_instance.intent] = skill_instance


    def dynamic_import(self, module_name, py_path):
        module_spec = spec_from_file_location(module_name, py_path)
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

if __name__ == '__main__':
    import jsonpickle
    s = Skills()
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

    