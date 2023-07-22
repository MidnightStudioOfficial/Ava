import tkinter as tk
from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTk, CTkButton
#from playsound import playsound
from PIL import Image, ImageTk

class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("300x200")

        # Load the background image
        self.bg_image = Image.open("Data/background.gif")
        self.bg_frames = [ImageTk.PhotoImage(self.bg_image)]
        try:
            while True:
                self.bg_image.seek(self.bg_image.tell() + 1)
                self.bg_frames.append(ImageTk.PhotoImage(self.bg_image))
        except EOFError:
            pass
        self.bg_frame = 0

        # Create the canvas
        self.canvas = tk.Canvas(self, width=300, height=200)
        self.canvas.pack(fill="both", expand=True)

        # Create the background image item
        self.bg_item = self.canvas.create_image(0, 0, image=self.bg_frames[0], anchor="nw")

        # Create the widgets
        self.text_label = CTkLabel(self.canvas, text="Loading...", font=("Arial", 16))
        self.text_label.pack(pady=(50, 10))

        self.progressbar = CTkProgressBar(self.canvas, orientation="horizontal", mode="determinate", width=250)
        self.progressbar.pack(pady=10)

        self.cancel_button = CTkButton(self.canvas, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=10)

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Start updating the background image
        self.update_background()

    def update_background(self):
        if len(self.bg_frames) > 1:
            self.bg_frame = (self.bg_frame + 1) % len(self.bg_frames)
            self.canvas.itemconfig(self.bg_item, image=self.bg_frames[self.bg_frame])
        self.after(100, self.update_background)

    def update_background2(self):
      self.bg_frame = (self.bg_frame + 1) % len(self.bg_frames)
      self.canvas.itemconfig(self.bg_item, image=self.bg_frames[self.bg_frame])
      self.after(100, self.update_background)

    def set_text(self, text):
        self.text_label.configure(text=text)

    def set_progress(self, value):
        try:
            # Update the progress bar and label
            self.progressbar.step(value)
        except Exception as e:
            # Add code here to handle the error
            pass

    def cancel(self):
        # Add code here to cancel the loading process
        pass


root = CTk()

splash_screen = SplashScreen(root)
#center(root)
splash_screen.set_text("Initializing...")
#splash_screen.set_progress(25)


splash_screen.set_text("Loading data...")
#splash_screen.set_progress(50)

splash_screen.set_text("Finalizing...")
#splash_screen.set_progress(100)


#splash_screen.progressbar.set(90)
#splash_screen.progressbar.set(1)
root.mainloop()
