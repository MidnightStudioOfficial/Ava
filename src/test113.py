from core.ui.wakeword.wakeword2 import WakeWordGUI
import customtkinter as ctk

def end_c():
    print("ENDED")

root = ctk.CTk()
w = WakeWordGUI(root, end_c)
root.mainloop()