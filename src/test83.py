import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import threading

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

        self.timer_label = ctk.CTkLabel(root, text="")
        self.timer_label.pack()

        self.exercise_label = ctk.CTkLabel(root, text="Choose an Exercise:")
        self.exercise_label.pack()

        self.exercise_options = [exercise["name"] for exercise in exercises]

        self.selected_exercise = ctk.StringVar(root)
        self.selected_exercise.set(self.exercise_options[0])  # Set the default exercise

        self.exercise_dropdown = ctk.CTkOptionMenu(root, variable=self.selected_exercise, values=self.exercise_options)
        self.exercise_dropdown.pack()

        self.start_button = ctk.CTkButton(root, text="Start", command=self.start_exercise)
        self.start_button.pack()

        # Breathing visualization
        self.canvas = ctk.CTkCanvas(root, width=200, height=200)
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

        # Create and start a separate thread for the timer
        self.timer_thread = threading.Thread(target=self.update_timer, args=(duration_seconds,), daemon=True)
        self.timer_thread.start()

        # Create and start a separate thread for the breathing visualization
        self.visualization_thread = threading.Thread(target=self.start_visualization, args=(duration_seconds,), daemon=True)
        self.visualization_thread.start()

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

    def start_visualization(self, duration):
        breath_cycles = 30  # Number of breath cycles for the visualization
        inhale_time = duration // (2 * breath_cycles)
        exhale_time = inhale_time

        self.animate_breathing(self.canvas, inhale_time, exhale_time, duration)

    def animate_breathing(self, canvas, inhale_time, exhale_time, duration):
        canvas.delete("all")

        def animate_inhale():
            for i in range(11):
                radius = 50 + (i * 10)
                canvas.delete("all")
                canvas.create_oval(100 - radius, 100 - radius, 100 + radius, 100 + radius, outline="blue", width=2)
                canvas.create_text(100, 100, text="Inhale", fill="blue")
                canvas.update()
                canvas.after(inhale_time * 1000 // 11)

        def animate_exhale():
            for i in range(10, -1, -1):
                radius = 50 + (i * 10)
                canvas.delete("all")
                canvas.create_oval(100 - radius, 100 - radius, 100 + radius, 100 + radius, outline="red", width=2)
                canvas.create_text(100, 100, text="Exhale", fill="red")
                canvas.update()
                canvas.after(exhale_time * 1000 // 11)

        # Start inhale animation
        animate_inhale()

        # Start exhale animation after inhale completes
        canvas.after(inhale_time * 1000, animate_exhale)

        # Repeat the breathing animation until the duration ends
        canvas.after(duration * 1000, self.reset_visualization, canvas)

    def reset_visualization(self, canvas):
        canvas.delete("all")

if __name__ == '__main__':
    root = ctk.CTk()
    app = MeditationApp(root)
    root.mainloop()
