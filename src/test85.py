import tkinter as tk
import customtkinter as ctk

root = ctk.CTk()
root.geometry("400x200")  # Set the size of the main window

# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create the first sub-frame
frame1 = ctk.CTkFrame(main_frame, bg_color="red", width=200, height=200)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for i in range(5):
    ctk.CTkLabel(frame1).pack()
    
# Create the second sub-frame
frame2 = ctk.CTkFrame(main_frame, bg_color="blue", width=200, height=200)
frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

for i in range(5):
    ctk.CTkLabel(frame2).pack()

root.mainloop()
