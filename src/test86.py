import tkinter as tk
import customtkinter as ctk

class CommandBarApp:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.show_button = ctk.CTkButton(self.master, text="Show Command Bar", command=self.show_command_bar)
        self.show_button.pack()
        self.hide_button = ctk.CTkButton(self.master, text="Hide Command Bar", command=self.hide_command_bar)
        self.hide_button.pack()

        self.frame = ctk.CTkFrame(self.master)

        self.output_text = ctk.CTkTextbox(self.frame)
        self.output_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.command_bar = ctk.CTkEntry(self.frame)
        self.hide_command_bar()

        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

    def show_command_bar(self):
        self.command_bar.pack(side=tk.TOP, fill=tk.X)
        self.output_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

    def hide_command_bar(self):
        self.command_bar.pack_forget()
        self.output_text.pack_forget()
        self.frame.pack_forget()

    def execute_command(self):
        command = self.command_bar.get()
        # Perform command execution here

        # Clear command bar
        self.command_bar.delete(0, tk.END)

        # Display command output in output area
        self.output_text.insert(tk.END, f">> {command}\n")
        self.output_text.insert(tk.END, "Command output goes here...\n")
        self.output_text.insert(tk.END, "\n")
        self.output_text.see(tk.END)  # Scroll to the bottom

if __name__ == "__main__":
    root = ctk.CTk()
    app = CommandBarApp(root)
    root.bind('<Return>', lambda event: app.execute_command())  # Bind Enter key press event
    root.mainloop()
