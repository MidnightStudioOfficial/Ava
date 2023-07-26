import tkinter as tk
import customtkinter as ctk
from core.base.global_vars import *


class MessagesController:
    def __init__(self, voice_engine=None, chat_frame=None, UserField=None, AITaskStatusLbl=None, current_chat_bubble=None, logo_image=None, chatbot=None) -> None:
        self.voice_engine = voice_engine
        self.chat_frame = chat_frame
        self.UserField = UserField
        self.AITaskStatusLbl = AITaskStatusLbl
        self.current_chat_bubble = current_chat_bubble
        self.logo_image = logo_image
        self.chatbot = chatbot

    def send_message(self, text: str):
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
        self.add_to_chat_history("You: " + user_message)
        self.AITaskStatusLbl.configure(text="    Working")
        if DEBUG_CHATBOT == None or DEBUG_CHATBOT == True:
            # Get response from chatbot and add to chat history
            bot_response = self.chatbot.get_response(user_message)
            self.add_to_chat_history("ChatBot: " + str(bot_response), True)

            # Use text-to-speech engine to speak the bot response
            self.voice_engine.say(bot_response)
            self.voice_engine.runAndWait()
            self.AITaskStatusLbl.configure(text="    Offline")

    def clearChatScreen(self):
        # Iterate through all the child widgets within the chat_frame
        # The chat_frame is a container holding the chat messages
        for wid in self.chat_frame.winfo_children():
            # Destroy each widget (chat message) to clear the chat screen
            # This effectively removes all the messages from the chat screen
            wid.destroy()

    def attach_to_frame(self, text, bot=False):
        """
        Attaches a chat message to the chat frame.

        Args:
            text (str): The text content of the message.
            bot (bool, optional): Indicates if the message is from the bot. Defaults to False.
        """
        if bot:
            # Create a chat label for bot message
            chat = ctk.CTkLabel(
                self.chat_frame,
                text=text,
                justify=tk.LEFT,
                wraplength=250,
                font=('Montserrat', 12, 'bold'),
                bg_color=botChatTextBg,
                corner_radius=7,
                anchor="s"
            )
            chat.pack(anchor='w', padx=5, pady=5)
        else:
            # Calculate the wraplength based on available space
            frame_width = self.chat_frame.winfo_width()
            wraplength = frame_width - 20  # Adjust wraplength dynamically based on chat_frame width and padding
            if wraplength < 100:
                wraplength = frame_width  # Set wraplength to frame width if it becomes too small

            # Create a chat label for user message
            chat = ctk.CTkLabel(
                self.chat_frame,
                text=text,
                justify=tk.RIGHT,
                wraplength=wraplength,
                font=('Montserrat', 12, 'bold'),
                fg_color=botChatTextBg,
                corner_radius=7,
            )

            # Update the wraplength if the text exceeds the available width
            chat.update_idletasks()
            text_width = chat.winfo_width()
            if text_width > wraplength:
                wraplength = text_width

            chat.configure(wraplength=wraplength)
            chat.pack(anchor='e', padx=2, pady=2)

    def show_image(self, image, direction='w'):
        """
        Displays an image in the chat frame.

        Args:
            image: The image to be displayed (Tkinter PhotoImage or PIL ImageTk).
            direction (str, optional): The anchor direction for the image. Defaults to 'w'.
                                    'w' for left (bot), 'e' for right (user).
        """
        chat = ctk.CTkLabel(
                self.chat_frame,
                text='',
                image=image,
                justify=tk.LEFT,
                wraplength=250,
                font=('Montserrat', 12, 'bold'),
                bg_color=botChatTextBg,
                corner_radius=7,
                anchor="s"
            )
        chat.pack(anchor=direction, padx=5, pady=5)

    def add_to_chat_history(self, message, bot=False):
        """
        Adds new text to the chat history.

        Parameters:
            message (str): The text message to be added to the chat history.
            bot (bool): A flag indicating whether the message is from the bot or not.
                        If True, it will be displayed with the bot's icon; otherwise, the user's icon.

        Note: The chat history consists of a vertical list of messages with alternating chat bubbles
            representing user and bot messages.

        """
        if self.current_chat_bubble == True:
            if bot is True:
                ctk.CTkLabel(self.chat_frame, image=self.logo_image, text="").pack(anchor='w', pady=0) #, bg=chatBgColor
                #self.show_image(self.logo_image)
            else:
                ctk.CTkLabel(self.chat_frame, text="").pack(anchor='e', pady=0) #, image=userIcon
            self.attach_to_frame(message, bot)
        elif self.current_chat_bubble == False:
            # Enable text editing and add message to chat history
            self.chat_frame.configure(state='normal')
            self.chat_frame.insert(tk.END, message + "\n")
            self.chat_frame.configure(state='disabled')

            # Automatically scroll to the bottom of the chat history
            self.chat_frame.yview(tk.END)
