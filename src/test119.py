import tkinter as tk
import numpy as np
import time

def linear_ease(t):
    return t

def ease_in_quad(t):
    return t**2

def ease_out_quad(t):
    return t * (2 - t)

def ease_in_out_cubic(t):
    return t * t * t * (t * (6 * t - 15) + 10)

def ease_in_elastic(t):
    c4 = (2 * np.pi) / 3
    return -(pow(2, 10 * (t - 1)) * np.sin((t * 10 - 1.75) * c4))

def animate_window_down(window, start_y, end_y, duration=1.0, easing_func=linear_ease):
    fps = 60
    total_frames = int(duration * fps)

    y_positions = np.linspace(start_y, end_y, total_frames)

    for frame in range(total_frames):
        t = frame / total_frames
        eased_t = easing_func(t)
        y_position = start_y + (end_y - start_y) * eased_t

        window.geometry(f"+{window.winfo_x()}+{int(y_position)}")
        window.update()
        time.sleep(1.0 / fps)

    # Add the bounce effect phase
    bounce_duration = 0.7  # Bounce effect duration in seconds 0.2
    bounce_frames = int(bounce_duration * fps)
    bounce_height = (end_y - start_y) * 0.6  # Adjust this value to control the bounce height 0.2

    for frame in range(bounce_frames):
        t = frame / bounce_frames
        eased_t = ease_out_bounce(t)
        y_position = end_y + bounce_height * eased_t

        window.geometry(f"+{window.winfo_x()}+{int(y_position)}")
        window.update()
        time.sleep(1.0 / fps)

def linear_ease(t):
    return t

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
    
def create_window(x, y):
    window = tk.Toplevel()
    window.geometry(f"300x200+{x}+{y}")
    return window

def main():
    # ... Your existing code ...
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Calculate the height of the screen
    screen_height = root.winfo_screenheight()

    # Create multiple windows
    window_info = [
        (create_window(400, 0), 0, screen_height - 200),
        (create_window(500, 0), 0, screen_height - 200),
        (create_window(600, 0), 0, screen_height - 200),
        (create_window(700, 0), 0, screen_height - 200)
    ]

    easing_functions = [linear_ease, ease_in_quad, ease_out_quad, ease_in_elastic]
    window_titles = ["linear_ease", "ease_in_quad", "ease_out_quad", "ease_in_elastic"]

    for i, (window, start_y, end_y) in enumerate(window_info):
        animate_window_down(window, start_y, end_y, duration=2.0, easing_func=easing_functions[i])
        window.title(window_titles[i])

    root.mainloop()

if __name__ == "__main__":
    main()
