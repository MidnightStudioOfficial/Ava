import tkinter as tk
import time

def animate_window_down(window, start_y, end_y, steps=100):
    for i in range(steps):
        y_position = start_y + (end_y - start_y) * (i + 1) / steps
        window.geometry(f"+{window.winfo_x()}+{int(y_position)}")
        window.update()
        time.sleep(0.02)  # Adjust the delay to control the speed of the animation

def main():
    root = tk.Tk()
    root.geometry("300x200+400+0")  # Set the initial position of the window

    # Calculate the height of the screen
    screen_height = root.winfo_screenheight()

    # Start the animation
    animate_window_down(root, 0, screen_height - 200)  # Moving 200 pixels above the bottom

    root.mainloop()

if __name__ == "__main__":
    main()
