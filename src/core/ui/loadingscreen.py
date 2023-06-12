import tkinter as tk
from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTk

class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("300x200")
        self.configure(background="white")
        
        # Create the widgets
        self.text_label = CTkLabel(self, text="Loading...", font=("Arial", 16))
        self.text_label.pack(pady=(50, 10))
        
        self.progressbar = CTkProgressBar(self, orientation="horizontal", mode="determinate", width=250)
        self.progressbar.pack(pady=10)
        
        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
    def set_text(self, text):
        self.text_label.configure(text=text)
        self.update()
    #@profile    
    def set_progress(self, value):
        self.progressbar.step()
        self.update()
        
if __name__ == '__main__':
    # Example usage
    root = CTk()

    splash_screen = SplashScreen(root)
    splash_screen.set_text("Initializing...")
    splash_screen.set_progress(25)

    # Do some work here...

    splash_screen.set_text("Loading data...")
    splash_screen.set_progress(50)

    # Do some more work here...

    splash_screen.set_text("Finalizing...")
    splash_screen.set_progress(100)

    root.mainloop()
