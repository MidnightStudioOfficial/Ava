from core.ui.settings.settings import SettingsUI
import customtkinter as ctk

root = ctk.CTk()
f = ctk.CTkFrame(root, fg_color="transparent")
f.pack()
s = SettingsUI(f)
root.mainloop()