from core.ui.loadingscreen2 import SplashScreen
import tkinter as tk
from customtkinter import CTk
import tkinter

root = CTk()

splash_screen = SplashScreen(root)
#center(root)
splash_screen.set_text("Initializing...")
#splash_screen.set_progress(25)

#import random
#import time
#while True:
#    splash_screen.set_text(str(random.randint(1, 50)))
#    splash_screen.set_progress(random.randint(1, 100))
#    #splash_screen.sp()
#    time.sleep(3)

splash_screen.set_text("Loading data...")
#splash_screen.set_progress(50)

splash_screen.set_text("Finalizing...")
#splash_screen.set_progress(100)
splash_screen.set_progress(50)
#splash_screen.progressbar.set(90)
#splash_screen.progressbar.set(1)
root.mainloop()
