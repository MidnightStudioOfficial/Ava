from core.skill.base_skill import BaseSkill
from pathlib import Path
from glob import glob
import os
from importlib.util import spec_from_file_location, module_from_spec


class Skills():

    skills = dict()

    def __init__(self, skills_path):
        path = skills_path  # Path(__file__).parent.resolve()
        modules = glob(str(path) + "/skills/**/*.py", recursive = True)
        for m in modules:
            module_name = os.path.split(m)[-1].strip(".py")
            imported_module = self.dynamic_import(module_name, m)
            # globals()[module_name] = imported_module
            # self.skills[module_name] = imported_module

        # for all subclasses of BaseSkill, instantiate and add them to the skills dict
        for concreteSkill in BaseSkill.__subclasses__():
            skill_instance = concreteSkill()
            self.skills[skill_instance.intent] = skill_instance

    def dynamic_import(self, module_name, py_path):
        module_spec = spec_from_file_location(module_name, py_path)
        module = module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
