import os
import json
from core.ui.signup.sign_up import SignUpApp

class ProfileChecker:
    def __init__(self) -> None:
        self.checker_data = None

    def check_if_profile_exists(self):
        """Check if a profile exists"""
        try:
            if os.path.exists("Data/profiles_metadata.json"):
                with open("Data/profiles_metadata.json", 'r') as file:
                    self.checker_data = json.load(file)
                    if self.checker_data["profile_created"] == True:
                        return True
                    return False
            else:
                self.__create_default_file()
                print("New file created with default data.")
                return False
        except Exception as e:
            print(f"Error loading profile metadata: {e}")
            return False

    def create_profile(self, root):
        """Start create a profile if no profile/profiles exist"""
        if self.check_if_profile_exists() == False:
            s = SignUpApp(root)

    def __create_default_file(self):
        """Create a profile metadata when it does not exist"""
        try:
            with open("Data/profiles_metadata.json", 'w') as file:
                self.checker_data = {
                    "profile_created": False
                }
                json.dump(self.checker_data, file)
        except Exception as e:
            print(f"Error saving profile metadata: {e}")
