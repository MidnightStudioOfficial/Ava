from core.ui.loadingscreen import SplashScreen
import tkinter as tk
from customtkinter import CTk
import tkinter

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    
root = CTk()

splash_screen = SplashScreen(root)
#center(root)
splash_screen.set_text("Initializing...")
splash_screen.set_progress(25)

import random
import time
#while True:
#    splash_screen.set_text(str(random.randint(1, 50)))
#    splash_screen.set_progress(random.randint(1, 100))
#    #splash_screen.sp()
#    time.sleep(3)

splash_screen.set_text("Loading data...")
splash_screen.set_progress(50)

splash_screen.set_text("Finalizing...")
splash_screen.set_progress(100)
splash_screen.set_progress(25)
root.mainloop()