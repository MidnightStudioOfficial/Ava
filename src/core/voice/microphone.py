import speech_recognition as sr

class VoiceMedium:
    def __init__(self, AITaskStatusLbl):
        """
        Initializes a new instance of the VoiceMedium class.

        :param AITaskStatusLbl: The label to display the AI task status.
        """
        self.AITaskStatusLbl = AITaskStatusLbl
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 4000

    def record(self):
        """
        Records audio from the microphone and returns the recognized text.

        :return: The recognized text, or 'None' if no speech was detected.
        """
        print('\nListening...')
        self.AITaskStatusLbl.configure(text="Listening...")
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source)
            # Record audio from the microphone
            audio = self.recognizer.listen(source)
            said = ""
            try:
                self.AITaskStatusLbl.configure(text="Processing...")
                # Recognize speech using Google Speech Recognition
                said = self.recognizer.recognize_google(audio)
                print(f"\nUser said: {said}")
            except Exception as e:
                print(e)
                return 'None'
        return said.lower()

    def voice_medium(self, chat_mode):
        """
        Continuously records audio from the microphone and sends the recognized text as a message.

        :param chat_mode: The chat mode. If 0, the method will exit.
        """
        while True:
            if chat_mode == 0:
                print("chatmode")
                break
            query = self.record()
            if query == 'None':
                continue
            self.send_message(query)
