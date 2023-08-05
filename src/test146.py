import re

class VirtualAssistant:
    def __init__(self):
        self.actions = {}

    def register_action(self, command):
        """Decorator to register actions in the actions dictionary."""
        def decorator(func):
            self.actions[command] = func
            return func
        return decorator

    @register_action("turn up the volume")
    def turn_up_volume(self):
        """Increase the volume."""
        print("Volume increased.")

    @register_action("turn down the volume")
    def turn_down_volume(self):
        """Decrease the volume."""
        print("Volume decreased.")

    @register_action("open notepad")
    def open_notepad(self):
        """Open the Notepad application."""
        print("Opening Notepad.")

    @register_action("set an alarm for (.+)")
    def set_alarm(self, time):
        """Set an alarm for a specific time."""
        print(f"Alarm set for {time}.")

    # Add more action methods here

    def process_command(self, command):
        """Process a user command."""
        matched_action = None
        for action_command, action_func in self.actions.items():
            match = re.match(action_command, command)
            if match:
                matched_action = action_func
                params = match.groups()  # Extract matched groups as parameters
                break
        
        if matched_action:
            try:
                matched_action(*params)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else:
            print("Command not recognized.")
