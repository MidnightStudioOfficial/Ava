import customtkinter as ctk
from PIL import Image
from core.AudioStream.output2 import AudioPlayer
import speech_recognition as sr
import threading
from wave import open as wav_open
import os


class WakeWordGUI(ctk.CTkToplevel):
    """Graphical User Interface (GUI) window for the Wake Word application."""

    def __init__(self, parent, end_callback) -> None:
        """
        Initialize the GUI window.

        Args:
            parent: The parent widget.
            end_callback: A function to call when the window is closed.
        """
        super().__init__(parent)
        from whisper import load_model
        self.title("Ava Screen")
        self.end_callback = end_callback
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.geometry("400x400")
        # self.overrideredirect(True)

        # Load images for the GUI elements
        self.photo = ctk.CTkImage(Image.open("Data/assets/ava_t.png"), size=(90, 90))
        self.pre_button_photo = Image.open("Data/images/centralButton1.png")
        self.button_photo = ctk.CTkImage(self.pre_button_photo, size=(self.pre_button_photo.width, self.pre_button_photo.height))
        self.pre_mic_button_photo = Image.open("Data/images/mic.png")
        self.mic_photo = ctk.CTkImage(self.pre_mic_button_photo, size=(50, 50))

        # Create the main frame and central image label
        self.MainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.MainFrame.pack(fill=ctk.BOTH)
        self.center_image = ctk.CTkLabel(self.MainFrame, text='', image=self.photo, height=90,  width=90)
        self.center_image.pack(pady=10, anchor='n')

        self.VoiceFrame = ctk.CTkFrame(self.MainFrame, fg_color="transparent")
        self.VoiceFrame.pack(fill=ctk.BOTH)
        # Create a CTkLabel object with the central button image and transparent foreground color
        self.cbl = ctk.CTkLabel(self.VoiceFrame, image=self.button_photo, fg_color="transparent")

        # Pack the central button label with a vertical padding of 17 pixels
        self.cbl.pack(pady=17)

        # Create a CTkLabel object with the text 'Offline', font size 16 and foreground color '#203647'
        self.AITaskStatusLbl = ctk.CTkLabel(self.VoiceFrame, text='    Offline', font=('montserrat', 16), fg_color="#203647")

        # Place the AI task status label at position (165, 32) in its parent widget
        self.AITaskStatusLbl.place(x=165, y=32)

        self.center_image2 = ctk.CTkButton(
            self.MainFrame,
            text='',
            image=self.mic_photo,
            height=50,
            width=50,
            command=self.on_mic_button_click
        )
        self.center_image2.pack(pady=10)

        # Initialize the audio player for sound feedback
        self.audio_player = AudioPlayer("Data/start.wav")

        # Create a recognizer object for speech recognition
        self.recognizer = sr.Recognizer()
        self.listening = False
        self.user_input = ""

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Load the Whisper speech recognition model
        self.model = load_model("tiny")

    def close_window(self):
        """Callback function for closing the GUI window."""
        del self.model
        self.audio_player.set_file("Data/back.wav")
        self.audio_player.play()
        print("closing")
        self.destroy()
        self.end_callback(self.user_input)

    def on_mic_button_click(self):
        """Callback function for the microphone button click."""
        # Play the microphone click sound
        self.audio_player.play_audio()
        if self.listening == False:
            # Start the speech recognition process in a new thread
            threading.Thread(target=self.listen_and_recognize, daemon=True).start()

    def listen_and_recognize(self):
        """
        Handle speech recognition when the microphone button is clicked.

        Uses the microphone to listen for speech and performs speech recognition.
        """
        if self.listening == False:
            try:
                # Start listening for speech using the microphone
                with sr.Microphone() as source:
                    print("Speak something...")
                    self.AITaskStatusLbl.configure(text="Listening..")
                    audio = self.recognizer.listen(source, timeout=7)
                    print("DONE")

                self.AITaskStatusLbl.configure(text="Thinking..")
                wav_filename = "TEMP_speech_audio.wav"
                with wav_open(wav_filename, 'wb') as wf:
                    wf.setnchannels(1)  # Mono channel
                    wf.setsampwidth(2)  # 2 bytes per sample
                    wf.setframerate(audio.sample_rate)  # Sample rate of the audio
                    wf.writeframes(audio.get_wav_data())

                # Use Whisper for speech recognition with numpy array
                print("transcribing")
                result = self.model.transcribe(wav_filename)
                text = result["text"]
                print("You said:", text)
                # Remove the temporary WAV file
                os.remove(wav_filename)
                self.AITaskStatusLbl.configure(text="Recognized: " + text)
                self.user_input = str(text)
                self.close_window()
                return

            except sr.WaitTimeoutError:
                # Handle microphone timeout error
                self.AITaskStatusLbl.configure(text="Listening timeout. Please try again.")
                return
            except sr.UnknownValueError:
                # Handle speech not recognized error
                self.AITaskStatusLbl.configure(text="Sorry, I could not understand what you said.")
                return
            except sr.RequestError as e:
                # Handle speech recognition API request error
                self.AITaskStatusLbl.configure(text="Error during recognition. Please check your internet connection.")
                return
            except Exception as e:
                # Handle any other unexpected errors
                print("Error:", e)
                self.AITaskStatusLbl.configure(text="Error during recognition. Please try again later.")
                return
