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
        
        #self.progress_label = CTkLabel(self, text="0%", font=("Arial", 12))
        #self.progress_label.pack(pady=10)
        
        self.cancel_button = CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=10)
        
        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Fade in the text and progress bar
        #alpha = 0.0
        #while alpha < 1.0:
        #    alpha += 0.1
        #    self.text_label.configure(fg_color=f"#{int(0xec * alpha):02x}{int(0xf0 * alpha):02x}{int(0xf1 * alpha):02x}")
        #    #self.progressbar.configure(fg_color=f"#3498db{int(alpha * 255):02x}")
        #    self.update()
        #    self.after(50)

        # alpha = 0.0
        # duration = 100000 # duration of the animation in milliseconds
        # start_time = time.time()
        # while alpha < 1.0:
        #     elapsed_time = time.time() - start_time
        #     alpha = easeInOutQuad(elapsed_time, 0, 1, duration)
        #     self.text_label.configure(text_color=f"#{int(0xec * alpha):02x}{int(0xf0 * alpha):02x}{int(0xf1 * alpha):02x}")
        #     self.update()
        #     self.after(10)

        
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
