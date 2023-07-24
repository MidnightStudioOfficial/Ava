import tkinter as tk
import customtkinter
from PIL import ImageTk, Image

class WelcomeApp(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.geometry("600x440")
        self.title('Welcome')
        img1 = ImageTk.PhotoImage(Image.open("Data/images/home2.jpg"))
        self.l1 = customtkinter.CTkLabel(master=self, image=img1)
        self.l1.pack()

        self.welcome_text = "Welcome to your very own virual assistant chatbot!"
        self.welcome_text2 = " This guide will help you get started and set up your chatbot to provide helpful and interactive text-based or voice-based conversations."

        self.create_page()

    def create_page(self):
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text=self.welcome_text, wraplength=240, font=customtkinter.CTkFont(size=16, weight="bold", family='Sans Serif'), text_color='#ffffff')
        self.l2.pack(pady=(30, 0))
        self.l3 = customtkinter.CTkLabel(master=self.frame, text=self.welcome_text2, wraplength=240, font=customtkinter.CTkFont(size=11, weight="bold", family='Arial'), text_color='#F5F5F5')
        self.l3.pack(pady=(3, 0))

        get_started_button = customtkinter.CTkButton(master=self.frame, width=100, text="Get Started")
        get_started_button.pack(pady=(30, 0))

    def create_profile(self):
        self.save_info()
        # Process the sign-up information from self.signup_info dictionary here
        print(self.get_started_info)

        self.destroy()  # Destroy current window and create new one


if __name__ == '__main__':
    root = customtkinter.CTk()
    s = WelcomeApp(root)
    root.mainloop()