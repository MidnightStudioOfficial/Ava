import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
from core.controllers.profile_create.profile import ProfileCreator

class SignUpApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.geometry("600x440")
        self.title('Create Profile')

        background_image = ImageTk.PhotoImage(Image.open("Data/images/home2.jpg"))
        self.background_label = customtkinter.CTkLabel(master=self, image=background_image)
        self.background_label.pack()

        self.pages = [
            {'label': 'Create your Profile', 'inputs': ['Username', 'Age']},
            {'label': 'Additional Information', 'inputs': ['Gender', 'Bio']},
            {'label': 'Confirmation', 'inputs': []}
        ]
        self.current_page = 0
        self.entries = []
        self.signup_info = {}

        self.create_page()

    def create_page(self):
        page = self.pages[self.current_page]
        self.background_label.configure(text=page['label'])

        frame = customtkinter.CTkFrame(master=self.background_label, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        for i, input_label in enumerate(page['inputs']):
            entry = customtkinter.CTkEntry(master=frame, width=220, placeholder_text=input_label)
            entry.place(x=50, y=110 + (i * 55))
            self.entries.append(entry)

        back_button = customtkinter.CTkButton(master=frame, width=100, text='Back', command=self.previous_page)
        back_button.place(x=50, y=300)

        if self.current_page < len(self.pages) - 1:
            next_button = customtkinter.CTkButton(master=frame, width=100, text='Next', command=self.next_page)
            next_button.place(x=170, y=300)
        else:
            create_button = customtkinter.CTkButton(master=frame, width=100, text='Create', command=self.create_profile)
            create_button.place(x=170, y=300)

    def next_page(self):
        """Go to the next page"""
        # Save the information from the current page
        # before moving to the next page
        self.save_info()
        # Increment the current_page counter to move to the next page
        self.current_page += 1
        # Clear the existing entries from the current page
        for entry in self.entries:
            entry.destroy()
        # Reset the entries list to prepare for the new page
        self.entries = []
        # Create the new page with fresh entries
        self.create_page()

    def previous_page(self):
        """Go back to the previous page"""
        # Check if the current page is greater than 0
        # (to avoid going below the first page)
        if self.current_page > 0:
            # Save the information from the current page before moving to the previous page
            self.save_info()
            # Decrement the current_page counter to move back to the previous page
            self.current_page -= 1
            # Clear the existing entries from the current page
            for entry in self.entries:
                entry.destroy()
            # Reset the entries list to prepare for the new page
            self.entries = []
            # Create the new page with fresh entries
            self.create_page()

    def save_info(self):
        current_page = self.pages[self.current_page]
        for i, input_label in enumerate(current_page['inputs']):
            value = self.entries[i].get()
            self.signup_info[input_label] = value

    def create_profile(self):
        self.save_info()
        # Process the sign-up information from self.signup_info dictionary here
        print(self.signup_info)
        creator = ProfileCreator(self.signup_info)
        creator.save_profile()

        self.destroy()  # Destroy current window and create new one
