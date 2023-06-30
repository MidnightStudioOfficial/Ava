from core.base.global_vars import *
import json

class Settings:
    def __init__(self) -> None:
        self.settings_data = None
        self.load_settings()

    def load_settings(self):
        try:
            with open("Data/settings.json", "r") as f:
                data = json.load(f)
                self.profile_data = data
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Invalid JSON syntax")

    def save_settings(self):
        try:
            with open("Data/settings.json", "w") as f:
                data = json.dump(self.profile_data, f)
        except FileNotFoundError:
            print("File not found")

    def set_setting(self, key, value):
        pass

    def get_setting(self, key, value):
        pass
