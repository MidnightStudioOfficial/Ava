from pyttsx3 import init as pyttsx3_init

class Voice:
     def __init__(self) -> None:
         # Set up voice
         self.engine = pyttsx3_init()
         self.voices = self.engine.getProperty('voices')
         self.engine.setProperty('voice', self.voices[2].id)  # Index 1 for female voice
         self.engine.setProperty('rate', 150)  # Adjust rate to 150 words per minute
         self.engine.setProperty('volume', 0.7)  # Adjust volume to 70% of maximum
         self.engine.setProperty('pitch', 110)  # Adjust pitch to 110% of default
      
     def __del__(self):
         print("Destructor called, cleaning up Voice class")
         if self.engine.isBusy == True:
             self.engine.stop()
         del self.engine
         del self.voices
     def say(self, text) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
     
     def change_voice(self, new_voice: int) -> None:
        self.engine.setProperty('voice', self.voices[new_voice].id)
    
     def change_rate(self, new_rate):
         """
         Adjust rate to words per minute
         new_rate: words per minute
         """
         self.engine.setProperty('rate', new_rate)  