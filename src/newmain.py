from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk
from os.path import join, dirname, realpath
import logging
from PIL import Image

chatMode = 1

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1 #0 for light, 1 for dark

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()



class ChatBotGUI:
    def __init__(self, master):
        self.master = master
        master.title("ChatBot")
        master.geometry("600x688")
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
        #w_width, w_height = 400, 650
        #s_width, s_height = master.winfo_screenwidth(), master.winfo_screenheight()
        #x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
        #master.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
       # root.configure(bg=background)
        # root.resizable(width=False, height=False)
        #self.second_frame.pack_propagate(0)

        self.profile_data = None
        self.root1 = ctk.CTkFrame(self.second_frame, bg_color=chatBgColor)
        self.root2 = ctk.CTkFrame(self.second_frame, bg_color=background)
        self.root3 = ctk.CTkFrame(self.second_frame, bg_color=background)

        for f in (self.root1, self.root2, self.root3):
            f.grid(row=0, column=0, sticky='news')    
        
        #self.canvas = ctk.CTkCanvas(parent, width=500, height=150)
        #self.canvas.pack()

        #self.profile_icon = ctk.CTkImage()
        self.chat_frame = ctk.CTkTextbox(self.root1, width=380,height=551,fg_color=chatBgColor)
        #self.profile_label.pack()
        self.chat_frame.pack(padx=10)
        #chat_frame.grid(padx=10)
        #self.chat_frame.pack_propagate(0)
        self.bottomFrame1 = ctk.CTkFrame(self.root1, height=100,fg_color="transparent", bg_color='#dfdfdf') #, bg_color='#dfdfdf'
        self.bottomFrame1.pack(fill=X, side=BOTTOM)
        #bottomFrame1.place(relx=0.5, rely=0.85, relwidth=0.7, relheight=0.1, anchor='n')
        self.VoiceModeFrame = ctk.CTkFrame(self.bottomFrame1,fg_color="transparent")
        self.VoiceModeFrame.pack(fill=BOTH)
        self.TextModeFrame = ctk.CTkFrame(self.bottomFrame1,fg_color="transparent") #, bg_color='#dfdfdf'
        self.TextModeFrame.pack(fill=BOTH)

        #self.VoiceModeFrame.pack_forget()
        self.TextModeFrame.pack_forget()

        self.cblLightImg = PhotoImage(file = "Data/images/centralButton.png") #ctk.CTkImage(Image.open(join(join(dirname(realpath(__file__)), "Data/images"), "centralButton.png")))
        self.cblDarkImg = PhotoImage(file = "Data/images/centralButton1.png")
        self.cblimage=self.cblDarkImg
        self.cbl = ctk.CTkLabel(self.VoiceModeFrame, image=self.cblimage, fg_color="transparent") #, fg_color='white', bg_color='#dfdfdf'
        self.cbl.pack(pady=17)
        self.AITaskStatusLbl = ctk.CTkLabel(self.VoiceModeFrame, text='    Offline', font=('montserrat', 16), fg_color="#203647") #, bg_color=AITaskStatusLblBG, fg_color='white'
        self.AITaskStatusLbl.place(x=165,y=32) #x=140 x=165
        
        
        #Keyboard Button
        self.kbphLight = PhotoImage(file = "Data/images/keyboard.png")
        self.kbphLight = self.kbphLight.subsample(2,2)
        self.kbphDark = PhotoImage(file = "Data/images/keyboard1.png")
        self.kbphDark = self.kbphDark.subsample(2,2)
        if KCS_IMG==1: self.kbphimage=self.kbphDark
        else: self.kbphimage=self.kbphLight
        self.kbBtn = ctk.CTkButton(self.VoiceModeFrame,text='',image=self.kbphimage,height=30,width=30, command=self.changeChatMode,fg_color="transparent") #, bg_color='#dfdfdf'
        self.kbBtn.place(x=25, y=30)

        #Mic
        self.micImg = PhotoImage(file = "Data/images/mic.png")
        self.micImg = self.micImg.subsample(2,2)
        self.micBtn = ctk.CTkButton(self.TextModeFrame,text='',image=self.micImg,height=30,width=30,fg_color="transparent", command=self.changeChatMode) #, bg_color='#dfdfdf'
        self.micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")    
        
        #Text Field
        self.TextFieldImg = PhotoImage(file='Data/images/textField.png')
        self.UserFieldLBL = ctk.CTkLabel(self.TextModeFrame,text='', image=self.TextFieldImg,fg_color="transparent") #, bg_color='#dfdfdf', text_color='white'
        #self.UserFieldLBL = ctk.CTkEntry(self.TextModeFrame, text_color='white', bg_color='#dfdfdf', font=('Montserrat', 16))
        self.UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
        self.UserField = ctk.CTkEntry(self.TextModeFrame, text_color='white', bg_color='#203647', font=('Montserrat', 16),width=304) #width=22
        self.UserField.place(x=16, y=30) #x=20
        self.UserField.insert(0, "Ask me anything...")
        self.UserField.bind('<Return>', lambda event: self.send_message())
        raise_frame(self.root1)
        #ProfileClass(self.second_frame, self)

        # Create chat history display
        #self.chat_history = ctk.CTkTextbox(self.second_frame, state='disabled', wrap='word', font=('Arial', 12)) #ScrolledText
        #self.chat_history.place(relx=0.5, rely=0.2, relwidth=0.95, relheight=0.6, anchor='n')

        # Create input field for user messages
        #self.user_input = ctk.CTkEntry(self.second_frame, font=('Arial', 12))
        #self.user_input.place(relx=0.5, rely=0.85, relwidth=0.7, relheight=0.1, anchor='n')

        # Create send button
        #self.send_button = ctk.CTkButton(self.second_frame, text="Send", command=self.send_message)
        #self.send_button.place(relx=0.85, rely=0.85, relwidth=0.15, relheight=0.1, anchor='n')

        # Bind enter key to send message
        #self.user_input.bind('<Return>', lambda event: self.send_message())

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
        
        # select default frame
        self.select_frame_by_name("home")
        


        # Delete useless stuff
        del image_path
        del self.large_test_image
        del self.home_image
        del self.chat_image
        del self.add_user_image
        del self.logo_image

  

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


    
    def changeChatMode(self):
        global chatMode
        if chatMode==1:
            # appControl.volumeControl('mute')
            self.VoiceModeFrame.pack_forget()
            self.TextModeFrame.pack(fill=BOTH)
            self.UserField.focus()
            chatMode=0
        else:
            # appControl.volumeControl('full')
            self.TextModeFrame.pack_forget()
            self.VoiceModeFrame.pack(fill=BOTH)
            #self.root.focus()
            chatMode=1
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
        user_message = self.UserField.get()
        self.UserField.delete(0, tk.END)

        # Add user message to chat history
        self._add_to_chat_history("You: " + user_message)

        # Get response from chatbot and add to chat history
        self._add_to_chat_history("ChatBot: ")

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
    print('Creating Ava Chatbot and taining')
    gui = ChatBotGUI(root)
    root.mainloop()