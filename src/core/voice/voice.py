"""
This module defines the Voice class, which utilizes the pyttsx3 library to provide text-to-speech functionality.
The Voice class allows setting up and configuring the speech engine, changing voice, adjusting speech rate, and
saying out text. It is intended to simplify the usage of the pyttsx3 library for text-to-speech conversion.

Required library:
- pyttsx3: A text-to-speech conversion library in Python.

Note:
- Before running this code, ensure that you have installed the pyttsx3 library.
- The pyttsx3 library might require additional dependencies to work correctly. Refer to the official documentation
  of pyttsx3 for installation and usage instructions.

Example Usage:
---------------
# Create a Voice object
voice = Voice()

# Say out a text
voice.say("Hello, this is an example text to be spoken out loud.")

# Change the speech rate
voice.change_rate(180)  # Set the speech rate to 180 words per minute.

# Change the voice
voice.change_voice(1)   # Set a different voice. (Use index corresponding to the desired voice.)

# Clean up the voice object (optional)
del voice

"""
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
        """
        Speak out the provided text.

        Parameters:
        text (str): The text to be spoken.
        """
        self.engine.say(text)
        self.engine.runAndWait()

     def change_voice(self, new_voice: int) -> None:
         """
         Change the voice used for speech.

         Parameters:
         new_voice (int): The index corresponding to the desired voice. (Use index of self.voices list)
         """
         self.engine.setProperty('voice', self.voices[new_voice].id)

     def change_rate(self, new_rate: int) -> None:
         """
         Adjust the speech rate to words per minute.

         Parameters:
         new_rate (int): The desired speech rate in words per minute.
         """
         self.engine.setProperty('rate', new_rate)
