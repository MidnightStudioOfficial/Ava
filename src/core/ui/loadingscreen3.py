import tkinter as tk
from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTk, CTkButton, CTkTooltip
from playsound import playsound
from PIL import Image, ImageTk

class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("300x200")
        
        # Load the background image
        self.bg_image = Image.open("background.gif")
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
        self.text_label = CTkLabel(self.canvas, text="Loading...", font=("Arial", 16), fg="#ecf0f1", bg="#2c3e50")
        self.text_label.pack(pady=(50, 10))
        
        self.progressbar = CTkProgressBar(self.canvas, orientation="horizontal", mode="determinate", width=250, fg="#3498db", bg="#2c3e50")
        self.progressbar.pack(pady=10)
        
        self.progress_label = CTkLabel(self.canvas, text="0%", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
        self.progress_label.pack(pady=10)
        
        self.cancel_button = CTkButton(self.canvas, text="Cancel", command=self.cancel, fg="#ecf0f1", bg="#e74c3c")
        self.cancel_button.pack(pady=10)
        
        # Add a tooltip to the cancel button
        self.cancel_tooltip = CTkTooltip(self.cancel_button, text="Click to cancel the loading process")
        
        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Fade in the text and progress bar
        alpha = 0.0
        while alpha < 1.0:
            alpha += 0.1
            self.text_label.configure(fg=f"#ecf0f1{int(alpha * 255):02x}")
            self.progressbar.configure(fg=f"#3498db{int(alpha * 255):02x}")
            self.update()
            self.after(50)
        
    def set_text(self, text):
        self.text_label.configure(text=text)
    
    def set_progress(self, value):
        try:
            # Update the progress bar and label
            self.progressbar.step(value)
            percent_complete = int(self.progressbar["value"] / self.progressbar["maximum"] * 100)
            if percent_complete == 100:
                playsound("complete.wav")
            self.progress_label.configure(text=f"{percent_complete}%")
            
            # Update the background image
            if len(self.bg_frames) > 1:
                self.bg_frame = (self.bg_frame + 1) % len(self.bg_frames)
                self.canvas.itemconfig(self.bg_item, image=self.bg_frames[self.bg_frame])
            
            # Update the display
            self.update()
            self.after(50)
            
        except Exception as e:
            # Add code here to handle the error
            pass
    
    def cancel(self):
        # Add code here to cancel the loading process
        pass
