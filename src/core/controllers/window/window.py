import tkinter as tk
import numpy as np
import time

class Animation:
    def __init__(self):
        self.fps = 60

    def linear_ease(self, t):
        return t

    def ease_in_quad(self, t):
        return t**2

    def ease_out_quad(self, t):
        return t * (2 - t)

    def ease_in_out_cubic(self, t):
        return t * t * t * (t * (6 * t - 15) + 10)

    def animate_window_down(self, window, start_y, end_y, duration=1.0, easing_func=linear_ease):
        total_frames = int(duration * self.fps)

        y_positions = np.linspace(start_y, end_y, total_frames)

        for frame in range(total_frames):
            t = frame / total_frames
            eased_t = easing_func(t)
            y_position = start_y + (end_y - start_y) * eased_t

            window.geometry(f"+{window.winfo_x()}+{int(y_position)}")
            window.update()
            time.sleep(1.0 / self.fps)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x100")
    root.title("Animated Window")

    animator = Animation()
    animator.animate_window_down(root, 100, 300, duration=2.0, easing_func=Animation.ease_in_out_cubic)

    root.mainloop()
