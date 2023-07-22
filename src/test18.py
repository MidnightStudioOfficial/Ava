from core.ui.loadingscreen2 import SplashScreen
from customtkinter import CTk

root = CTk()

splash_screen = SplashScreen(root)
splash_screen.set_text("Initializing...")
splash_screen.set_text("Loading data...")
splash_screen.set_text("Finalizing...")
splash_screen.set_progress(50)
root.mainloop()
