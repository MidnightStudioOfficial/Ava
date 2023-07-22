import tkinter as tk

def fade_out(window, alpha=1.0, delay=30, step=0.05):
    if alpha > 0:
        window.attributes('-alpha', alpha)
        window.after(delay, fade_out, window, alpha - step, delay, step)
    else:
        window.destroy()

def create_fade_out_window():
    fade_window = tk.Toplevel()
    fade_window.title("Fading Window")
    fade_window.geometry("300x200")
    fade_window.attributes('-alpha', 1.0)

    fade_out(fade_window)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("400x300")

    fade_out_button = tk.Button(root, text="Create Fading Window", command=create_fade_out_window)
    fade_out_button.pack(pady=20)

    root.mainloop()
