import tkinter as tk
from tkinter import messagebox

# Exercise data
exercises = [
    {
        "name": "Deep Breathing",
        "description": "Take slow, deep breaths in and out.",
        "duration": 5  # in minutes
    },
    {
        "name": "Body Scan",
        "description": "Scan your body for any tension or discomfort.",
        "duration": 10
    },
    # Add more exercises here
]

class MeditationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meditation App")

        self.timer_label = tk.Label(root, text="")
        self.timer_label.pack()

        self.exercise_label = tk.Label(root, text="Choose an Exercise:")
        self.exercise_label.pack()

        self.exercise_options = [exercise["name"] for exercise in exercises]

        self.selected_exercise = tk.StringVar(root)
        self.selected_exercise.set(self.exercise_options[0])  # Set the default exercise

        self.exercise_dropdown = tk.OptionMenu(root, self.selected_exercise, *self.exercise_options)
        self.exercise_dropdown.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_exercise)
        self.start_button.pack()

    def start_exercise(self):
        selected_exercise = self.selected_exercise.get()
        exercise = [ex for ex in exercises if ex["name"] == selected_exercise][0]
        self.exercise_name = exercise["name"]
        self.exercise_description = exercise["description"]
        duration_minutes = exercise["duration"]
        duration_seconds = duration_minutes * 60

        # Display a message box with exercise details
        messagebox.showinfo("Exercise", f"Exercise: {self.exercise_name}\nDuration: {duration_minutes} minutes")

        self.update_timer(duration_seconds)  # Start the timer

    def update_timer(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"Time Remaining: {minutes:02d}:{seconds:02d}"
        self.timer_label.configure(text=timer_text)

        if remaining_time > 0:
            self.root.after(1000, self.update_timer, remaining_time - 1)
        else:
            self.show_next_exercise()

    def show_next_exercise(self):
        # Display a message box to indicate the end of the exercise
        messagebox.showinfo("Exercise", "Exercise completed!")

        # Start the next exercise
        self.start_exercise()


root = tk.Tk()
app = MeditationApp(root)
root.mainloop()
