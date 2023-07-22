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
    return t ** 3 + (t * t * t * (t * (6 * t - 15) + 10))


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


def linear_ease(t):
    return t



def create_window(x, y):
    window = tk.Toplevel()
    window.geometry(f"300x200+{x}+{y}")
    return window

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Calculate the height of the screen
    screen_height = root.winfo_screenheight()

    # Create multiple windows
    window1 = create_window(400, 0)
    window2 = create_window(500, 0)
    window3 = create_window(600, 0)
    window4 = create_window(700, 0)

    # Animate each window with different easing functions
    animate_window_down(window4, 0, screen_height - 200, duration=4.0, easing_func=ease_in_out_cubic)
    window4.title("ease_in_out_cubic")


    root.mainloop()

if __name__ == "__main__":
    main()
