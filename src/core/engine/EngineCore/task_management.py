class TaskManager:
    def __init__(self):
        self.actions = {
            "turn up the volume": self.turn_up_volume,
            "turn down the volume": self.turn_down_volume,
            "(?:set|change)\s+(?:the\s+)?volume\s+(?:to\s+|at\s+)?(\d+)\b": self.turn_up_volume,
            "open notepad": self.open_notepad,
            # Add more actions here
        }

    def turn_up_volume(self):
        """Increase the volume."""
        print("Volume increased.")

    def turn_down_volume(self):
        """Decrease the volume."""
        print("Volume decreased.")

    def open_notepad(self):
        """Open the Notepad application."""
        print("Opening Notepad.")

    # Add more action methods here

    def process_command(self, command):
        """Process a user command."""
        action = self.actions.get(command, None)
        if action:
            action()
        else:
            print("Command not recognized.")

def main():
    assistant = TaskManager()

    while True:
        user_input = input("Enter a command: ").lower()
        if user_input == "exit":
            print("Exiting the virtual assistant.")
            break
        assistant.process_command(user_input)

if __name__ == "__main__":
    main()
