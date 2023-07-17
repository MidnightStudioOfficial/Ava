import tkinter as tk
from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTk, CTkButton


class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("300x200")
        self.configure(background="#2c3e50")
        
        # Create the widgets
        self.text_label = CTkLabel(self, text="Loading...", font=("Arial", 16)) #, fg_color="#ecf0f1", bg_color="#2c3e50"
        self.text_label.pack(pady=(50, 10))
        
        self.progressbar = CTkProgressBar(self, orientation="horizontal", mode="determinate", width=250)
        self.progressbar.pack(pady=10)
        
        self.cancel_button = CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=10)
        
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
    
    def set_progress(self, value):
        try:
            for i in range(value):
             self.progressbar.step()
            #percent_complete = int(100 - self.progressbar.get())
            #self.progress_label.configure(text=f"{percent_complete}%")
            self.update()
        except Exception as e:
            # Add code here to handle the error
            pass
    
    def cancel(self):
        # Add code here to cancel the loading process
        pass
