import tkinter as tk
import random
import time

# Motivational quotes
quotes = [
    "Believe you can and you're halfway there.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Don't watch the clock; do what it does. Keep going.",
    "The only way to do great work is to love what you do.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts."
]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity App")

        self.timer_running = False
        self.timer_seconds = 0
        self.pomodoro_count = 0

        self.create_widgets()

    def create_widgets(self):
        # Timer
        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 36))
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Timer", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack()

        # Stopwatch
        self.stopwatch_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 36))
        self.stopwatch_label.pack(pady=10)

        self.start_stopwatch_button = tk.Button(self.root, text="Start Stopwatch", command=self.start_stopwatch)
        self.start_stopwatch_button.pack()

        self.stop_stopwatch_button = tk.Button(self.root, text="Stop Stopwatch", command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_stopwatch_button.pack()

        # Motivational Quote
        self.quote_label = tk.Label(self.root, text="", font=("Helvetica", 14), wraplength=400)
        self.quote_label.pack(pady=10)

        self.show_quote_button = tk.Button(self.root, text="Show Motivational Quote", command=self.show_quote)
        self.show_quote_button.pack()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.stopwatch_label.config(text="00:00:00")
            self.stop_stopwatch_button.config(state=tk.DISABLED)
            self.timer()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def timer(self):
        if self.timer_running:
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            hours = minutes // 60
            minutes = minutes % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Check if a Pomodoro cycle is completed
            if self.timer_seconds % 1500 == 0:
                self.pomodoro_count += 1
                self.show_quote()
                if self.pomodoro_count % 4 == 0:
                    self.timer_label.config(text="Time for a long break!")
                    self.stop_timer()
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.pomodoro_count = 0
                    return

            self.root.after(1000, self.timer)

    def start_stopwatch(self):
        self.start_stopwatch_button.config(state=tk.DISABLED)
        self.stop_stopwatch_button.config(state=tk.NORMAL)
        self.timer_label.config(text="00:00:00")
        self.stop_timer()
        self.stopwatch_running = True
        self.start_time = time.time()
        self.stopwatch()

    def stop_stopwatch(self):
        self.start_stopwatch_button.config(state=tk.NORMAL)
        self.stop_stopwatch_button.config(state=tk.DISABLED)
        self.stopwatch_running = False

    def stopwatch(self):
        if self.stopwatch_running:
            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            hours = int(minutes // 60)
            minutes = int(minutes % 60)
            self.stopwatch_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.stopwatch)

    def show_quote(self):
        quote = random.choice(quotes)
        self.quote_label.config(text=quote)

root = tk.Tk()
app = App(root)
root.mainloop()
