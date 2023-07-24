import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from core.AudioStream.output2 import AudioPlayer
import speech_recognition as sr


class WakeWordGUI(ctk.CTkToplevel):
    def __init__(self, parent, end_callback) -> None:
        super().__init__(parent)
        self.title("Ava Screen")
        self.end_callback = end_callback
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.geometry("400x400")
        #self.overrideredirect(True)
        photo = ctk.CTkImage(Image.open("Data/assets/ava_t.png"), size=(90,90))
        self.pre_button_photo = Image.open("Data/images/centralButton1.png")
        self.button_photo = ctk.CTkImage(self.pre_button_photo, size=(self.pre_button_photo.width, self.pre_button_photo.height))
        self.pre_mic_button_photo = Image.open("Data/images/mic.png")
        self.mic_photo = ctk.CTkImage(self.pre_mic_button_photo, size=(50, 50))
        self.MainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.MainFrame.pack(fill=ctk.BOTH)
        self.center_image = ctk.CTkLabel(
            self.MainFrame,
            text='',
            image=photo,
            height=90,
            width=90
        )
        self.center_image.pack(pady=10, anchor='n')
        self.VoiceFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent")
        self.VoiceFrame.pack(fill=ctk.BOTH)
        #self.center_label = ctk.CTkLabel(self.VoiceFrame, text='Starting')
        #self.center_label.pack(pady=10)
        # Create a CTkLabel object with the central button image and transparent foreground color
        self.cbl = ctk.CTkLabel(self.VoiceFrame, image=self.button_photo, fg_color="transparent")

        # Pack the central button label with a vertical padding of 17 pixels
        self.cbl.pack(pady=17)

        # Create a CTkLabel object with the text 'Offline', font size 16 and foreground color '#203647'
        self.AITaskStatusLbl = ctk.CTkLabel(self.VoiceFrame, text='    Listening', font=('montserrat', 16), fg_color="#203647")

        # Place the AI task status label at position (165, 32) in its parent widget
        self.AITaskStatusLbl.place(x=165, y=32)

        self.center_image2 = ctk.CTkButton(self.MainFrame, text='', image=self.mic_photo, height=50, width=50, command=self.mic_click)
        self.center_image2.pack(pady=10)

        self.audio = AudioPlayer("Data/start.wav")
        # Create a recognizer object
        self.recognizer = sr.Recognizer()
        self.listening = False

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def close_window(self):
        print("closeing")
        self.end_callback()
        self.destroy()

    def mic_click(self):
        #self.audio.play_audio()
        if self.listening == False:
            #self.AITaskStatusLbl.configure(text="Listening..")

            # Use the microphone as a source
            with sr.Microphone() as source:
                print("Speak something...")
                #self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = self.recognizer.listen(source)

            try:
                self.AITaskStatusLbl.configure(text="Thinking..")
                # Recognize speech using Google Web Speech API
                text = self.recognizer.recognize_google(audio)
                print("You said:", text)
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio.")
            except sr.RequestError as e:
                print("Could not request results from Google Web Speech API; {0}".format(e))

            #self.listening = True
