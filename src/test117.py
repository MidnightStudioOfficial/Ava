import numpy as np
import tkinter as tk
from tkinter import ttk

# Easing functions
def linear_ease(x):
    return x

def quadratic_ease(x):
    return x ** 2

def cubic_ease(x):
    return x ** 3
def ease_out_bounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375
def hg(t):
    return t ** 3 + (t * t * t * (t * (6 * t - 15) + 10)) / 4.654 / ease_out_bounce(t)

# Create the Tkinter application
root = tk.Tk()
root.title("Animation Easing Graph Editor")

canvas_width = 400
canvas_height = 200

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

def draw_easing_graph():
    easing_type = easing_combo.get()

    # Clear the canvas
    canvas.delete("all")

    # Draw the axes
    canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill='black', width=2)
    canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill='black', width=2)

    # Draw the easing graph
    x_values = np.linspace(-1, 1, canvas_width)
    if easing_type == 'Linear':
        y_values = [linear_ease(x) for x in x_values]
    elif easing_type == 'Quadratic':
        y_values = [quadratic_ease(x) for x in x_values]
    elif easing_type == 'Cubic':
        y_values = [cubic_ease(x) for x in x_values]
    elif easing_type == 'hg':
        y_values = [hg(x) for x in x_values]

    scaled_y_values = [(canvas_height / 2) - (y * canvas_height / 2) for y in y_values]

    for i in range(len(x_values) - 1):
        x1, y1 = x_values[i], scaled_y_values[i]
        x2, y2 = x_values[i + 1], scaled_y_values[i + 1]
        canvas.create_line(canvas_width / 2 + x1 * canvas_width / 2, y1, canvas_width / 2 + x2 * canvas_width / 2, y2, fill='blue', width=2)

easing_options = ['Linear', 'Quadratic', 'Cubic', 'hg']  # Add more easing functions as needed
easing_combo = ttk.Combobox(root, values=easing_options, state='readonly')
easing_combo.pack()

easing_combo.set('Linear')  # Set the default easing function

# Call the draw_easing_graph function whenever the user selects a different easing function
easing_combo.bind("<<ComboboxSelected>>", lambda event: draw_easing_graph())

draw_easing_graph()  # Initial drawing of the easing graph

root.mainloop()
