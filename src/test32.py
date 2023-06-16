import tkinter as tk
from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTk, CTkButton, CTkCanvas
#from playsound import playsound
from PIL import Image, ImageTk

class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Splash Screen")
        self.geometry("300x200")
        
        # Load the background image
        self.bg_image = Image.open("Data/background.gif")
        self.bg_frames = []
        self.bg_item = None
        self.bg_image_frame = None  # Initialize the attribute
        # Create the canvas
        self.canvas = CTkCanvas(self, width=300, height=200)
        self.canvas.pack(fill="both", expand=True)
        
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
        try:
            self.bg_image.seek(self.bg_image.tell() + 1)
            frame = ImageTk.PhotoImage(self.bg_image)
            if self.bg_item:
                self.canvas.delete(self.bg_item)
            self.bg_item = self.canvas.create_image(0, 0, image=frame, anchor="nw")
            self.bg_image_frame = frame  # Store the current frame
        except EOFError:
            self.bg_image.seek(0)  # Go back to the first frame
        self.after(100, self.update_background)



    def set_text(self, text):
        self.text_label.configure(text=text)
    
    def set_progress(self, value):
        try:
            # Update the progress bar and label
            self.progressbar.step(value)
            #percent_complete = int(self.progressbar["value"] / self.progressbar["maximum"] * 100)
            #if percent_complete == 100:
            #    playsound("complete.wav")
            #self.progress_label.configure(text=f"{percent_complete}%")
            
            # Update the display
            self.update()
            
        except Exception as e:
            # Add code here to handle the error
            pass
    
    def cancel(self):
        # Add code here to cancel the loading process
        pass


from customtkinter import CTk


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
