import time
import tkinter as tk
from tkinter import ttk


def print_progress_bar(iteration, total, progress_bar):
    percent = int(100 * (iteration / float(total)))
    progress_bar['value'] = percent
    progress_bar.update()

    average_time = calculate_average_time(iteration)
    estimated_time = calculate_estimated_time(iteration, total, average_time)
    status_label.config(text=f"Progress: {percent}% | ETA: {estimated_time} | Avg: {average_time:.2f}s")

    if iteration == total:
        status_label.config(text="Task complete!")

def calculate_estimated_time(iteration, total, average_time):
    remaining_iterations = total - iteration
    estimated_time = average_time * remaining_iterations
    hours = int(estimated_time // 3600)
    minutes = int((estimated_time % 3600) // 60)
    seconds = int(estimated_time % 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def calculate_average_time(iteration):
    if iteration == 0:
        return 0

    elapsed_time = time.perf_counter() - start_time
    average_time = elapsed_time / iteration
    return average_time

def simulate_task(total_iterations):
    for i in range(total_iterations):
        # Simulating some task
        time.sleep(0.1)

        # Update the progress bar
        print_progress_bar(i + 1, total_iterations, progress_bar)

# Create the GUI
root = tk.Tk()
root.title("Progress Bar")
root.geometry("400x100")

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Status Label
status_label = ttk.Label(root, text="Progress: 0%")
status_label.pack()

# Start the task
total_iterations = 100
start_time = time.perf_counter()
simulate_task(total_iterations)

# Run the GUI
root.mainloop()
