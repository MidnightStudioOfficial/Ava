import tkinter as tk
from tkinter import *
import tkinter as tk
#from tkinter import ttk
#from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk

def mouse_wheel(event):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

root = tk.Tk()
root.geometry("400x300")

# Create a canvas and a vertical scrollbar
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<MouseWheel>", mouse_wheel)

# Create a frame inside the canvas for scrolling content
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
chatMode = 1

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
def attach_to_frame(text, bot=False):
    if bot:
        chat = ctk.CTkLabel(
            scrollable_frame,
            text=text,
            justify=LEFT,
            wraplength=250,
            font=('Montserrat', 12, 'bold'),
            corner_radius=7,
            bg_color=botChatTextBg,
        )
        chat.pack(anchor='w', padx=5, pady=5)
    else:
        chat = ctk.CTkLabel(
            scrollable_frame,
            text=text,
            justify=RIGHT,
            wraplength=250,
            fg_color=botChatTextBg,
            font=('Montserrat', 12, 'bold'),
            corner_radius=7
        )

        chat.pack(anchor='e', padx=5, pady=5)

    # Adjust the chat label's alignment based on the chat mode
    if chatMode == 1:
        if bot:
            chat.configure(justify=LEFT, anchor='s')
        else:
            chat.configure(justify=RIGHT, anchor='s')
    else:
        if bot:
            chat.configure(justify=LEFT, anchor='n')
        else:
            chat.configure(justify=RIGHT, anchor='n')

    chat.update_idletasks()  # Update the chat label

    # Check if the scroll position is at the end
    scroll_pos = scrollable_frame.winfo_height() - canvas.winfo_height()
    if scroll_pos <= canvas.yview()[1]:
        canvas.yview_moveto(1.0)  # Scroll to the bottom

    scrollable_frame.update_idletasks()  # Update the scrollable frame
    canvas.update_idletasks()  # Update the canvas



# Add some content to the scrollable frame
for i in range(5):
    attach_to_frame("hi", bot=True)
for i in range(5):
    attach_to_frame("hello", bot=False)
root.mainloop()
