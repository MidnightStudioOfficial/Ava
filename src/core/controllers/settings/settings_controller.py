import json


class SettingsController:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as file:
                settings_data = json.load(file)
                return settings_data
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or has invalid JSON, return an empty dictionary
            return {}

    def save_settings(self):
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

# Example usage
if __name__ == "__main__":
    controller = SettingsController("settings.json")

    # Get a setting
    theme = controller.get_setting("theme", "light")
    print("Theme:", theme)

    # Set a setting
    controller.set_setting("theme", "dark")

    # Get the updated setting
    updated_theme = controller.get_setting("theme")
    print("Updated Theme:", updated_theme)
