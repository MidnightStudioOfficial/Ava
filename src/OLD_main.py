# Author: MidnightStudioOfficial
# License: MIT
# Description: This is the main script that connects and runs everything
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk
from os.path import join, dirname, realpath
import logging
from PIL import Image

#print('Importing chatterbot')
#from chatterbot import ChatBot as CHATBOT
#from chatterbot.trainers import ChatterBotCorpusTrainer
print('Importing pyttsx3')
from pyttsx3 import init as pyttsx3_init
#import spacy

print("Importing user_profile")
import user_profile

print("Importing chatbot")
from core.chatbot.chatbot import Chatbot
print("Importing DONE")

logging.basicConfig(level=logging.INFO)

class ChatBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")
        master.geometry("600x600")
        #master.resizable(False, False)
        # set grid layout 1x2
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        
        self.min_w = 50 # Minimum width of the frame
        self.max_w = 200 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded
        
        image_path = join(dirname(realpath(__file__)), "Data/assets")
        self.logo_image = ctk.CTkImage(Image.open(join(image_path, "my-Ava.png")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(join(image_path, "text.png")), size=(290, 118)) #size=(500, 150)
        self.image_icon_image = ctk.CTkImage(Image.open(join(image_path, "home.png")), size=(20, 20))
        
        self.home_image = ctk.CTkImage(light_image=Image.open(join(image_path, "home.png")), dark_image=Image.open(join(image_path, "home.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(join(image_path, "chat.png")), dark_image=Image.open(join(image_path, "chat.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(join(image_path, "settings.png")), dark_image=Image.open(join(image_path, "settings.png")), size=(20, 20))
        self.add_DNA_image = ctk.CTkImage(light_image=Image.open(join(image_path, "DNA.png")), dark_image=Image.open(join(image_path, "DNA.png")), size=(20, 20))
        
        
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(master, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Ava", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Chat",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_DNA_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="DNA",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_DNA_image, anchor="w", command=self.frame_DNA_button_event)
        self.frame_DNA_button.grid(row=4, column=0, sticky="ew")
        
        self.frame_profile_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Profile",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_DNA_image, anchor="w", command=self.frame_profile_button_event)
        self.frame_profile_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        
        # create home frame
        self.home_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = ctk.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = ctk.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")

        # Create chat history display
        self.chat_history = ctk.CTkTextbox(self.second_frame, state='disabled', wrap='word', font=('Arial', 12)) #ScrolledText
        self.chat_history.place(relx=0.5, rely=0.2, relwidth=0.95, relheight=0.6, anchor='n')

        # Create input field for user messages
        self.user_input = ctk.CTkEntry(self.second_frame, font=('Arial', 12))
        self.user_input.place(relx=0.5, rely=0.85, relwidth=0.7, relheight=0.1, anchor='n')

        # Create send button
        self.send_button = ctk.CTkButton(self.second_frame, text="Send", command=self.send_message)
        self.send_button.place(relx=0.85, rely=0.85, relwidth=0.15, relheight=0.1, anchor='n')

        # Bind enter key to send message
        self.user_input.bind('<Return>', lambda event: self.send_message())

        # create third frame
        self.third_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        
        # create the DNA frame
        self.DNA_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        
        self.DNA_frame_large_label = ctk.CTkLabel(self.DNA_frame, text="DNA: Create A new chatbot!", font=ctk.CTkFont(family='Lucida Console', size=15, weight="bold")) #, font=ctk.CTkFont(size=15, weight="bold")
        self.DNA_frame_large_label.grid(row=0, column=0, padx=20, pady=10)
        self.DNA_frame_large_label.place(relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        self.DNA_label_gender = ctk.CTkLabel(self.DNA_frame, text="Gender") #, font=('MV Boli', 12)
        self.DNA_label_gender.place(relx=0.5, rely=0.16666, anchor=tk.CENTER)
        self.DNA_combobox_gender = ctk.CTkOptionMenu(self.DNA_frame, values=["Male", "Female"])
        self.DNA_combobox_gender.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        # create the profile frame
        self.profile_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        user_profile.ProfileClass(self.profile_frame, self)

        
        # select default frame
        self.select_frame_by_name("home")
        
        # Set up voice
        self.engine = pyttsx3_init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)  # Index 1 for female voice
        self.engine.setProperty('rate', 150)  # Adjust rate to 150 words per minute
        self.engine.setProperty('volume', 0.7)  # Adjust volume to 70% of maximum
        self.engine.setProperty('pitch', 110)  # Adjust pitch to 110% of default

        # Delete useless stuff
        del image_path
        del self.large_test_image
        del self.home_image
        del self.chat_image
        del self.voices
        del self.add_user_image
        del self.logo_image

        # Initialize chatbot
        self.chatbot = Chatbot()
        self.chatbot.train_bot() # Train the chatbot
  

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_DNA_button.configure(fg_color=("gray75", "gray25") if name == "frame_DNA" else "transparent")
        self.frame_profile_button.configure(fg_color=("gray75", "gray25") if name == "frame_profile" else "transparent")

        # show selected frame
        if name == "home": # home
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2": # chat
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3": # settings
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_DNA": # DNA
            self.DNA_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.DNA_frame.grid_forget()
        if name == "frame_profile": # profile
            self.profile_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.profile_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        
    def frame_DNA_button_event(self):
        self.select_frame_by_name("frame_DNA")
        
    def frame_profile_button_event(self):
        self.select_frame_by_name("frame_profile")

    def change_appearance_mode_event(self, new_appearance_mode):
        """
        Change the GUI appearance mode
        """
        ctk.set_appearance_mode(new_appearance_mode)  
        
    def send_message(self):
        # Get user input and clear input field
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)

        # Add user message to chat history
        self._add_to_chat_history("You: " + user_message)

        # Get response from chatbot and add to chat history
        bot_response = self.chatbot.get_response(user_message)
        self._add_to_chat_history("ChatBot: " + bot_response)
        self.engine.say(bot_response)
        self.engine.runAndWait()

    def _add_to_chat_history(self, message):
        """
        Adds new text to the chat history
        """
        # Enable text editing and add message to chat history
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.configure(state='disabled')
        # Automatically scroll to the bottom of the chat history
        self.chat_history.yview(tk.END)

# class ChatBot:
#     def __init__(self):
#         # Initialize chatbot model here
#         self.nlp = spacy.load("en_core_web_sm")
#         self.chatbot_exists = None
#         if os.path.isfile("./db.sqlite3") == False:
#             logging.debug("chatbot_exists is False")
#             self.chatbot_exists = False
#         else:
#             logging.debug("chatbot_exists is True")
#             self.chatbot_exists = True

#         self.chatBot = CHATBOT("Chatbot", tagger_language=self.nlp)
#         #self.chatBot = ChatBot("Chatbot", tagger_language="en")
#         self.trainer = ChatterBotCorpusTrainer(self.chatBot)

#         pass
    
#     def train_bot(self):
#         logging.debug("Training bot")
#         if self.chatbot_exists == False:
#          self.trainer.train("./Data/training/export.json")
#          self.trainer.train("./Data/training/messages.json")
#          #del self.trainer     

#     def get_response(self, user_message):
#        bot = self.chatBot.get_response(text=user_message,search_text=user_message)
#        print(bot.text)
#        return bot.text

if __name__ == '__main__':
    print('Creating GUI')
    root = ctk.CTk() #tk.Tk()
    print('Creating Ava Chatbot and taining')
    gui = ChatBotGUI(root)
    root.mainloop()