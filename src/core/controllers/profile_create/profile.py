import json
import os

class ProfileCreator:
    def __init__(self, profile_data) -> None:
        self.profile_data = profile_data
        self.profile_data_TEMP = {
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Hello my name is John Doe",
                "gender": "male",
                "interests": ["Python programming", "Web development", "Data science"],
                "achievements_1": True,
                "achievements_2": True,
                "achievements_3": True
          }

    def load_profile(self):
        pass

    def __change_profile_checker(self):
        try:
            with open("Data/profiles_metadata.json", 'w') as file:
                self.checker_data = {
                    "profile_created": True
                }
                json.dump(self.checker_data, file)
        except Exception as e:
            print(f"Error saving profile metadata: {e}")

    def save_profile(self):
        try:
            self.profile_data_TEMP["first_name"] = self.profile_data["Username"]
            self.profile_data_TEMP["last_name"] = self.profile_data["Username"]
            self.profile_data_TEMP["bio"] = self.profile_data["Bio"]
            self.profile_data_TEMP["gender"] = self.profile_data["Gender"]

            with open("Data/profile/profile.json", 'w') as file:
                json.dump(self.profile_data_TEMP, file)

            self.__change_profile_checker()
            print("Profile saved successfully.")
        except Exception as e:
            print(f"Error saving profile: {e}")
