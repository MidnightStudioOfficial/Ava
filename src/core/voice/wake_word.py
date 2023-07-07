from core.voice.mic import SpeechRecognizer

class WakeWord:
    def __init__(self, gui_callback) -> None:
        self.detecter = SpeechRecognizer(callback_function=self.detected)
        self.gui_callback = gui_callback
    
    def start(self):
        print("starting wakeword")
        self.detecter.start_listening()
    
    def detected(self, text):
        print("detected:"+str(text))
        self.gui_callback(text)