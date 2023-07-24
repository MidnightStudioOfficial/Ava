from queue import Queue
from threading import Thread
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, wake_words=("ava", "eva", "hangover"), callback_function=None):
        self.wake_words = wake_words # "hava", "java", "lava"
        self.r = sr.Recognizer()
        self.words_queue = []
        self.audio_queue = Queue()
        self.recognize_thread = None
        self.callback = callback_function
        self.stoping = False

    def check_for_wakeword(self, text):
        if any(wake_word in text for wake_word in self.wake_words):
            print("I can hear you")
            self.callback(text)

    def recognize_worker(self):
        # This runs in a background thread
        while True:
            audio = self.audio_queue.get()  # Retrieve the next audio processing job from the main thread
            if audio is None:
                break  # Stop processing if the main thread is done

            # Received audio data, now we'll recognize it using Google Speech Recognition
            try:
                # For testing purposes, we're just using the default API key
                # To use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # Instead of `r.recognize_google(audio)`
                text = self.r.recognize_google(audio)
                self.check_for_wakeword(str(text).lower())
                print("Google Speech Recognition thinks you said: " + str(text))
                self.words_queue.append(str(text))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service: {0}".format(e))

            self.audio_queue.task_done()  # Mark the audio processing job as completed in the queue
            #self.audio_queue.

    def _start_listening(self):
        # Start a new thread to recognize audio while this thread focuses on listening
        self.recognize_thread = Thread(target=self.recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()
        print("Starting")
        with sr.Microphone() as source:
            try:
                while True:  # Repeatedly listen for phrases and put the resulting audio on the audio processing job queue
                    if self.stoping == True:
                        #source.audio.close()
                        print("Stoping mic")
                        break
                    self.audio_queue.put(self.r.listen(source))
            except KeyboardInterrupt:  # Allow Ctrl + C to shut down the program
                pass

        self.audio_queue.join()  # Block until all current audio processing jobs are done
        self.audio_queue.put(None)  # Tell the recognize_thread to stop
        self.recognize_thread.join()  # Wait for the recognize_thread to actually stop

    def stop_listening(self):
        self.stoping = True
        #print("self.recognize_thread2.join()")
        #self.recognize_thread2.
        #print("DONE")
        return
        print("self.audio_queue.put(None)")
        self.audio_queue.put(None)
        print("audio_queue.join()")
        self.audio_queue.join()
        print("self.recognize_thread.join()")
        self.recognize_thread.join()
        print("self.recognize_thread2.join()")
        self.recognize_thread2.join()
        print("DONE")

    def start_listening(self):
        self.stoping = False
        self.recognize_thread2 = Thread(target=self._start_listening)
        self.recognize_thread2.daemon = True
        self.recognize_thread2.start()
        #self._start_listening()    

# Create an instance of the SpeechRecognizer class and start listening
#if __name__ == "__main__":
#   recognizer = SpeechRecognizer()
#    recognizer.start_listening()
