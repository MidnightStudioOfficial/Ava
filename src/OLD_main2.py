from tkinter import *
import tkinter as tk
import customtkinter as ctk
from os.path import join, dirname, realpath
import logging
from PIL import Image
from threading import Thread

DEBUG_CHATBOT = None # None
DEBUG_GUI = None
PEODUCTION = None

print("Importing user_profile")
import user_profile

print("Importing skills_page")
from core.ui.skills.skills_page import SkillGUI

print("Importing loadingscreen")
from core.ui.loadingscreen2 import SplashScreen

print("Importing Debug")
from core.base.debug import DebugGUI

if DEBUG_CHATBOT == None or DEBUG_CHATBOT == True:
    
 print('Importing pyttsx3')
 from pyttsx3 import init as pyttsx3_init

 print("Importing chatbot")
 from core.chatbot.chatbot import Chatbot

print("Importing DONE")

logging.basicConfig(level=logging.INFO)

chatMode = 1

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1 # 0 for light, 1 for dark

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()

class ChatBotGUI:
    def __init__(self, master, splash_screen):
        # Initialize the ChatBotGUI object
        self.master = master

        # Set the title and geometry of the master window
        master.title("ChatBot")
        master.geometry("600x688")

        # Prevent the master window from being resized (commented out)
        # master.resizable(False, False)

        # Set the grid layout to 1 row and 2 columns
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.min_w = 50 # Minimum width of the frame
        self.max_w = 200 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded

        # Set the path to the image assets
        image_path = join(dirname(realpath(__file__)), "Data/assets")

        # Create CTkImage objects for various images
        splash_screen.set_text("Loading Images")
        self.logo_image = ctk.CTkImage(Image.open(join(image_path, "ava.jfif")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(join(image_path, "Welcome.png")), size=(290, 118))
        self.image_icon_image = ctk.CTkImage(Image.open(join(image_path, "home.png")), size=(20, 20))
        self.image_weather_icon_image = ctk.CTkImage(Image.open(join(image_path, "weather.png")), size=(20, 20))
        self.image_news_icon_image = ctk.CTkImage(Image.open(join(image_path, "news.png")), size=(20, 20))
        self.image_fire_icon_image = ctk.CTkImage(Image.open(join(image_path, "fire.png")), size=(20, 20))

        
        self.home_image = ctk.CTkImage(light_image=Image.open(join(image_path, "home.png")), dark_image=Image.open(join(image_path, "home.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(join(image_path, "chat.png")), dark_image=Image.open(join(image_path, "chat.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(join(image_path, "settings.png")), dark_image=Image.open(join(image_path, "settings.png")), size=(20, 20))
        self.add_DNA_image = ctk.CTkImage(light_image=Image.open(join(image_path, "DNA.png")), dark_image=Image.open(join(image_path, "DNA.png")), size=(20, 20))
        
        
        # create navigation frame
        splash_screen.set_text("Creating gui")
        self.navigation_frame = ctk.CTkFrame(master, corner_radius=7) # corner_radius=0
        # Place the navigation frame in the grid layout at row 0 and column 0
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        # Create a CTkLabel object for the navigation frame label with text "Ava", an image, and font size 15
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Ava", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Create CTkButton objects for the home, chat, settings, DNA, and profile buttons
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
        
        self.frame_skills_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Skills",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_DNA_image, anchor="w", command=self.frame_skills_button_event)
        self.frame_skills_button.grid(row=6, column=0, sticky="ew")
        
        # Create an option menu for selecting the appearance mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                    command=self.change_appearance_mode_event)

        # Place the appearance mode menu in the grid layout at row 6 and column 0 with padding
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        
        # create home frame
        self.home_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        # create welcome image
        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_label_1 = ctk.CTkLabel(self.home_frame, text="Welcome back!", font=ctk.CTkFont(family='Lucida Console', size=15, weight="bold")) # Welcome text
        self.home_frame_label_1.grid(row=1, column=0, padx=20, pady=10)
        #self.home_frame_button_1 = ctk.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        #self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = ctk.CTkButton(self.home_frame, text="Get the Weather", image=self.image_weather_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = ctk.CTkButton(self.home_frame, text="Read the News", image=self.image_news_icon_image, compound="right")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = ctk.CTkButton(self.home_frame, text="Get Cozy and Chat", image=self.image_fire_icon_image, compound="right", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        version_button = ctk.CTkButton(master, text="V1.0", width=96, command=self.debug_click)
        version_button.grid(sticky="se", column=1)
        
        # create second frame
        self.second_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")

        # Create three frames with different background colors
        self.root1 = ctk.CTkFrame(self.second_frame, bg_color=chatBgColor)
        self.root2 = ctk.CTkFrame(self.second_frame, bg_color=background)
        self.root3 = ctk.CTkFrame(self.second_frame, bg_color=background)

        # Grid all frames to the same cell in the grid layout
        # This will cause the frames to overlap each other
        for f in (self.root1, self.root2, self.root3):
            f.grid(row=0, column=0, sticky='news')

        self.chat_frame = ctk.CTkTextbox(self.root1, width=380, height=551, fg_color=chatBgColor)
        self.chat_frame.pack(padx=10)
        #self.chat_frame.pack_propagate(0)
        
        # Create a new CTkFrame object with height 100, transparent foreground color and '#dfdfdf' background color
        self.bottomFrame1 = ctk.CTkFrame(self.root1, height=100, fg_color="transparent", bg_color='#dfdfdf')

        # Pack the bottomFrame1 to fill the X direction and be placed at the bottom of its parent widget
        self.bottomFrame1.pack(fill=X, side=BOTTOM)

        # Create a new CTkFrame object with transparent foreground color
        self.VoiceModeFrame = ctk.CTkFrame(self.bottomFrame1, fg_color="transparent")

        # Pack the VoiceModeFrame to fill both X and Y directions
        self.VoiceModeFrame.pack(fill=BOTH)

        # Create a new CTkFrame object with transparent foreground color
        self.TextModeFrame = ctk.CTkFrame(self.bottomFrame1, fg_color="transparent")

        # Pack the TextModeFrame to fill both X and Y directions
        self.TextModeFrame.pack(fill=BOTH)

        self.TextModeFrame.pack_forget()
        
        # Create PhotoImage objects for the light and dark central button images
        self.cblLightImg = PhotoImage(file="Data/images/centralButton.png")
        self.cblDarkImg = PhotoImage(file="Data/images/centralButton1.png")

        # Set the current central button image to the dark image
        self.cblimage = self.cblDarkImg

        # Create a CTkLabel object with the central button image and transparent foreground color
        self.cbl = ctk.CTkLabel(self.VoiceModeFrame, image=self.cblimage, fg_color="transparent")

        # Pack the central button label with a vertical padding of 17 pixels
        self.cbl.pack(pady=17)

        # Create a CTkLabel object with the text 'Offline', font size 16 and foreground color '#203647'
        self.AITaskStatusLbl = ctk.CTkLabel(self.VoiceModeFrame, text='    Offline', font=('montserrat', 16), fg_color="#203647")

        # Place the AI task status label at position (165, 32) in its parent widget
        self.AITaskStatusLbl.place(x=165, y=32)
        
        # Keyboard Button
        self.kbphLight = PhotoImage(file="Data/images/keyboard.png")
        self.kbphLight = self.kbphLight.subsample(2, 2)

        self.kbphDark = PhotoImage(file="Data/images/keyboard1.png")
        self.kbphDark = self.kbphDark.subsample(2, 2)

        if KCS_IMG == 1:
            self.kbphimage = self.kbphDark
        else:
            self.kbphimage = self.kbphLight

        self.kbBtn = ctk.CTkButton(
            self.VoiceModeFrame,
            text='',
            image=self.kbphimage,
            height=30,
            width=30,
            command=self.changeChatMode,
            fg_color="transparent"
        )
        self.kbBtn.place(x=25, y=30)

        # Mic
        self.micImg = PhotoImage(file="Data/images/mic.png")
        self.micImg = self.micImg.subsample(2, 2)
        self.micBtn = ctk.CTkButton(self.TextModeFrame,text='',image=self.micImg,height=30,width=30,fg_color="transparent", command=self.changeChatMode)
        self.micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")    
        
        # Text Field
        self.TextFieldImg = PhotoImage(file='Data/images/textField.png')
        self.UserFieldLBL = ctk.CTkLabel(self.TextModeFrame,text='', image=self.TextFieldImg, fg_color="transparent") #, bg_color='#dfdfdf', text_color='white'
        self.UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
        self.UserField = ctk.CTkEntry(self.TextModeFrame, text_color='white', bg_color='#203647', font=('Montserrat', 16),width=304) #width=22
        self.UserField.place(x=16, y=30) #x=20
        self.UserField.insert(0, "Ask me anything...")
        self.UserField.bind('<Return>', lambda event: self.send_message(None))
        raise_frame(self.root1)

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

        # create the skills frame
        self.skills_frame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        SkillGUI(self.skills_frame)

        # select default frame
        self.select_frame_by_name("home")

        if DEBUG_CHATBOT == None or DEBUG_CHATBOT == True:
         # Set up voice
         splash_screen.set_text("Set up voice")
         self.engine = pyttsx3_init()
         self.voices = self.engine.getProperty('voices')
         self.engine.setProperty('voice', self.voices[2].id)  # Index 1 for female voice
         self.engine.setProperty('rate', 150)  # Adjust rate to 150 words per minute
         self.engine.setProperty('volume', 0.7)  # Adjust volume to 70% of maximum
         self.engine.setProperty('pitch', 110)  # Adjust pitch to 110% of default
         del self.voices

        # Delete useless stuff
        splash_screen.set_text("Deleting useless stuff")
        del image_path
        del self.large_test_image
        del self.home_image
        del self.chat_image
        del self.add_user_image
        del self.logo_image
        
        self.recognize_thread = None
        self.stoped_lisening = False
        
        if DEBUG_CHATBOT == None or DEBUG_CHATBOT == True:
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
        self.frame_skills_button.configure(fg_color=("gray75", "gray25") if name == "frame_skills" else "transparent")

        # show selected frame
        if name == "home":  # home
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":  # chat
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":  # settings
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_DNA":  # DNA
            self.DNA_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.DNA_frame.grid_forget()
        if name == "frame_profile":  # profile
            self.profile_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.profile_frame.grid_forget()
        if name == "frame_skills":  # skills
            self.skills_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.skills_frame.grid_forget()

    def debug_click(self):
        DebugGUI(self.master)

    def record(self, clearChat=True, iconDisplay=True):
        import speech_recognition as sr
        print('\nListening...')
        self.AITaskStatusLbl.configure(text="Listening...")
        r = sr.Recognizer()
        r.dynamic_energy_threshold = False
        r.energy_threshold = 4000
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            said = ""
            try:
                self.AITaskStatusLbl.configure(text="Processing...")
                said = r.recognize_google(audio)
                print(f"\nUser said: {said}")
            except Exception as e:
                print(e)
                return 'None'
        return said.lower()

    def voiceMedium(self):
        while True:
          if chatMode == 0:
              print("chatmode")
              break
          query = self.record()
          if query == 'None': continue
          self.send_message(query)

    def changeChatMode(self):
        global chatMode
        if chatMode == 1:
            # If the current chat mode is 1 (voice mode)
            # Mute the volume (commented out)
            # appControl.volumeControl('mute')

            # Hide the VoiceModeFrame and show the TextModeFrame
            self.VoiceModeFrame.pack_forget()
            self.TextModeFrame.pack(fill=BOTH)

            # Set focus to the UserField
            self.UserField.focus()

            # Set the chat mode to 0 (text mode)
            chatMode = 0
            if type(self.recognize_thread) == type(Thread):
                self.recognize_thread.join()
        else:
            # If the current chat mode is not 1 (text mode)
            # Set the volume to full (commented out)
            # appControl.volumeControl('full')

            # Hide the TextModeFrame and show the VoiceModeFrame
            self.TextModeFrame.pack_forget()
            self.VoiceModeFrame.pack(fill=BOTH)


            # Set focus to the root window (commented out)
            # self.root.focus()

            # Set the chat mode to 1 (voice mode)
            chatMode = 1
            try:
                # pass
                if type(self.recognize_thread) != type(Thread):
                 self.recognize_thread = Thread(target=self.voiceMedium, daemon=True).start()
            except:
                pass

    def home_button_event(self):
        self.select_frame_by_name("home")
        # #self.skill_gui = None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        # #self.skill_gui = None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass
    
    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        # #self.skill_gui = None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass
        
    def frame_DNA_button_event(self):
         self.select_frame_by_name("frame_DNA")
        # #self.skill_gui = None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass
        
    def frame_profile_button_event(self):
         self.select_frame_by_name("frame_profile")
        # #self.skill_gui = None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass
    
    def frame_skills_button_event(self):
        # #if self.skill_gui == None
        # try:
        #  #del self.skill_gui
        #  self.skill_gui = None
        # except:
        #     pass
        # #self.skill_gui = SkillGUI(self.skills_frame)
        # if self.skill_gui is None or not self.skill_gui.winfo_exists():
        #     self.skill_gui = SkillGUI(self.skills_frame) # create window if its None or destroyed
        # else:
        #     pass
        
        #     #self.toplevel_window.focus()  # if window exists focus it
        self.select_frame_by_name("frame_skills")


    def change_appearance_mode_event(self, new_appearance_mode):
        """
        Change the GUI appearance mode
        """
        ctk.set_appearance_mode(new_appearance_mode)  
        
    def send_message(self, text: None):
        """
        Sends a message from the user to the chatbot and displays the bot's response.

        This method gets the user input from the UserField, clears the input field, and adds the user message to the chat history.
        If DEBUG_CHATBOT is None or True, the method gets a response from the chatbot and adds it to the chat history.
        It also uses a text-to-speech engine to speak the bot response.
        """
        # Get user input and clear input field
        if text == None:
         user_message = self.UserField.get()
         self.UserField.delete(0, tk.END)
        else:
            user_message = text

        # Add user message to chat history
        self._add_to_chat_history("You: " + user_message)
        self.AITaskStatusLbl.configure(text="    Working")
        if DEBUG_CHATBOT == None or DEBUG_CHATBOT == True:
            # Get response from chatbot and add to chat history
            bot_response = self.chatbot.get_response(user_message)
            self._add_to_chat_history("ChatBot: " + str(bot_response))

            # Use text-to-speech engine to speak the bot response
            self.engine.say(bot_response)
            self.engine.runAndWait()
            self.AITaskStatusLbl.configure(text="    Offline")
            


    def _add_to_chat_history(self, message):
        """
        Adds new text to the chat history
        """
        # Enable text editing and add message to chat history
        self.chat_frame.configure(state='normal')
        self.chat_frame.insert(tk.END, message + "\n")
        self.chat_frame.configure(state='disabled')

        # Automatically scroll to the bottom of the chat history
        self.chat_frame.yview(tk.END)


if __name__ == '__main__':
    print('Creating GUI')
    root = ctk.CTk()
    splash_screen = SplashScreen(root)
    splash_screen.overrideredirect(True)
    splash_screen.set_text("Creating Ava Chatbot and taining")
    splash_screen.set_progress(50)
    print('Creating Ava Chatbot and taining')
    gui = ChatBotGUI(root, splash_screen)
    splash_screen.set_text("Done")
    splash_screen.set_progress(100)
    splash_screen.destroy()
    root.mainloop()