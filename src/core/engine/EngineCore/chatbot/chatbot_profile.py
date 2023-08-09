import json


class ChatbotProfile:
      def __init__(self) -> None:
        print("Importing brain (This may take a while!)")
        from core.brain.brain import Brain
        self.profile_data = {
              "name": None,
              "gender": None,
              "brain": {
                   "traits": [],
                   "mood": None,
                   "thought": None,
                   "memory": {}
              }
        }
        self.brain = Brain()
        self.brain.start()

      def update_profile(self):
          self.profile_data["brain"]["mood"] = self.brain.mood
          self.profile_data["brain"]["thought"] = self.brain.thought

      def _set_profile_data(self):
          self.brain.mood = self.profile_data["brain"]["mood"]
          self.brain.thought = self.profile_data["brain"]["thought"]

      def load_profile(self):
        # Open the JSON file
        try:
         with open('./Data/chatbot/profile.json', 'r') as f:
             # Load the contents of the file as a Python object
             data = json.load(f)
             self.profile_data["name"] = data["name"]
             self.profile_data["gender"] = data["gender"]
             self.profile_data["brain"]["traits"] = data["brain"]["traits"]
             self.profile_data["brain"]["mood"] = data["brain"]["mood"]
             self.profile_data["brain"]["thought"] = data["brain"]["thought"]
             self.profile_data["brain"]["memory"] = data["brain"]["memory"]
        except FileNotFoundError:
           print("File not found")
        except json.JSONDecodeError:
           print("Invalid JSON syntax")
        self._set_profile_data()

      def save_profile(self):
       self.update_profile()
       try:
            with open('./Data/chatbot/profile.json', 'w') as f:
                # Load the contents of the file as a Python object
                data = json.dump(self.profile_data, f)
       except FileNotFoundError:
           print("File not found")
       except json.JSONDecodeError:
           print("Invalid JSON syntax")
