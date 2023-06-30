import tkinter as tk
import customtkinter
from PIL import ImageTk, Image

class SignUpApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.geometry("600x440")
        self.title('Create Profile')

        img1 = ImageTk.PhotoImage(Image.open("Data/images/home2.jpg"))
        self.l1 = customtkinter.CTkLabel(master=self, image=img1)
        self.l1.pack()

        self.pages = [
            {'label': 'Create your Account', 'inputs': ['Username', 'Age']},
            {'label': 'Additional Information', 'inputs': ['Email', 'Phone']},
            {'label': 'Confirmation', 'inputs': []}
        ]
        self.current_page = 0
        self.entries = []

        self.create_page()

    def create_page(self):
        page = self.pages[self.current_page]
        self.l1.configure(text=page['label'])

        frame = customtkinter.CTkFrame(master=self.l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for i, input_label in enumerate(page['inputs']):
            entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text=input_label)
            entry.place(x=50, y=110 + (i * 55))
            self.entries.append(entry)

        back_button = customtkinter.CTkButton(master=frame, width=100, text="Back", command=self.previous_page)
        back_button.place(x=50, y=300)

        if self.current_page < len(self.pages) - 1:
            next_button = customtkinter.CTkButton(master=frame, width=100, text="Next", command=self.next_page)
            next_button.place(x=170, y=300)
        else:
            create_button = customtkinter.CTkButton(master=frame, width=100, text="Create", command=self.create_profile)
            create_button.place(x=170, y=300)

    def next_page(self):
        self.current_page += 1
        for entry in self.entries:
            entry.destroy()
        self.entries = []
        self.create_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            for entry in self.entries:
                entry.destroy()
            self.entries = []
            self.create_page()

    def create_profile(self):
        # Process the sign-up information here
        self.destroy()  # Destroy current window and create new one
        w = customtkinter.CTk()
        w.geometry("1280x720")
        w.title('Welcome')
        l1 = customtkinter.CTkLabel(master=w, text="Home Page", font=('Century Gothic', 60))
        l1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        w.mainloop()