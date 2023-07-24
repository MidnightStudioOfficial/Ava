import os
import json

class Profile:
    def __init__(self) -> None:
        self.profile_data = None

    def list_profiles(self):
        new_profile_list = []
        profile_list = os.listdir("Data/profile")
        for profile_file in profile_list:
            root, ext = os.path.splitext(profile_file)
            new_profile_list.append(root)
        return new_profile_list

    def load_profile(self):
        try:
            if os.path.exists("Data/profile/profile.json"):
                with open("Data/profile/profile.json", "r") as f:
                    data = json.load(f)
                    self.profile_data = data
            else:
                self.profile_data = {
                    "first_name": "N/A",
                    "last_name": "N/A",
                    "bio": "N/A",
                    "gender": "N/A",
                    "interests": ["N/A"],
                    "achievements_1": True,
                    "achievements_2": True,
                    "achievements_3": True
                }
        except json.JSONDecodeError:
            print("Invalid JSON syntax")
