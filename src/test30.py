import tkinter as tk
import customtkinter as ctk

class RightClickMenu(ctk.CTkToplevel):
    def __init__(self, master, items):
        super().__init__(master)
        self.withdraw()  # Hide the menu initially
        self.overrideredirect(True)  # Remove window decorations
        self.items = items

        self.bind('<FocusOut>', lambda event: self.withdraw())  # Hide menu when it loses focus

        # Create menu items
        for item in self.items:
            label = ctk.CTkLabel(self, text=item)
            label.pack()

            # Add command to each item (replace print_message with desired functionality)
            label.bind('<Button-1>', lambda event, text=item: self.print_message(text))

    def show(self, x, y):
        self.geometry('+{}+{}'.format(x, y))  # Position the menu
        self.deiconify()  # Show the menu

    def print_message(self, text):
        print("Selected:", text)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bind('<Button-3>', self.show_menu)  # Bind right-click event to the main window
        self.menu = RightClickMenu(self, ['Item 1', 'Item 2', 'Item 3'])  # Create the custom menu

    def show_menu(self, event):
        self.menu.show(event.x_root, event.y_root)  # Show the menu at the mouse position


app = Application()
app.mainloop()
