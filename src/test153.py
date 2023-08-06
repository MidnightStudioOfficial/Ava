import customtkinter
from core.ui.settings.settings import SettingsUI

root = customtkinter.CTk()
f = customtkinter.CTkFrame(root)
SettingsUI(f)
f.pack()
root.mainloop()