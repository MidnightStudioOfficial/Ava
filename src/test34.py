import tkinter as tk

def fade_out(window, alpha=1.0):
    alpha -= 0.1  # Decrease the alpha value for transparency
    window.attributes('-alpha', alpha)  # Set the new alpha value

    if alpha > 0:
        # Call the fade_out function again after a delay
        window.after(100, fade_out, window, alpha)
    else:
        window.destroy()  # Close the window when the fade-out is complete

def create_window():
    window = tk.Toplevel(root)
    window.geometry('200x200')
    window.attributes('-alpha', 1.0)  # Set initial alpha value to fully opaque

    # Bind the window close event to initiate fade-out
    window.protocol('WM_DELETE_WINDOW', lambda: fade_out(window))

root = tk.Tk()
button = tk.Button(root, text='Create Window', command=create_window)
button.pack()

root.mainloop()
