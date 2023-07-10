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

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

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
        self.start_animation()

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

    def start_animation(self):
        self.canvas.delete("all")  # Clear canvas
        radius = 100
        self.canvas.create_oval(150 - radius, 150 - radius, 150 + radius, 150 + radius, outline="blue", width=2)
        self.canvas.create_text(150, 150, text="Breathe", font=("Helvetica", 24))

        # Animation parameters
        breath_in_duration = 4  # seconds
        breath_out_duration = 4  # seconds

        # Calculate animation intervals based on exercise duration
        exercise = [ex for ex in exercises if ex["name"] == self.exercise_name][0]
        duration_minutes = exercise["duration"]
        total_animation_duration = (breath_in_duration + breath_out_duration) * (duration_minutes // 2)
        interval = int((total_animation_duration * 1000) / (radius * 2))

        self.animate_breathing(radius, breath_in_duration, breath_out_duration, interval)

    def animate_breathing(self, radius, breath_in_duration, breath_out_duration, interval):
        self.canvas.itemconfigure("all", fill="white")  # Change color to white for breathing in
        self.canvas.update()

        self.canvas.after(interval, lambda: self.canvas.itemconfigure("all", fill="blue"))  # Change color to blue for breathing out
        self.canvas.after(breath_in_duration * 1000, lambda: self.canvas.itemconfigure("all", fill="white"))
        self.canvas.after(breath_out_duration * 1000, lambda: self.animate_breathing(radius, breath_in_duration, breath_out_duration, interval))


root = tk.Tk()
app = MeditationApp(root)
root.mainloop()
