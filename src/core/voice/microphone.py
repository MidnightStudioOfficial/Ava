from threading import Thread, Lock
from queue import Queue
import speech_recognition as sr

class SpeechRecognizer:
    
    def __init__(self, wake_words=("ava", "eva")):
        self.wake_words = wake_words # "hava", "java", "lava"
        self.r = sr.Recognizer()
        self.audio_queue = Queue()
        self.recognize_thread = None
        self.audio_queue_lock = Lock()

    def check_for_wakeword(self, text):
        if any(wake_word in text for wake_word in self.wake_words):
            print("I can hear you")
            #command = text.split(wake_word, 1)[1].strip()
            #self.handle_command(command)

    def recognize_worker(self):
        while True:
            with self.audio_queue_lock:
                audio = self.audio_queue.get()
            if audio is None:
                break

            try:
                text = self.r.recognize_google(audio)
                self.check_for_wakeword(str(text).lower())
                print("Google Speech Recognition thinks you said: " + str(text))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service: {0}".format(e))

            with self.audio_queue_lock:
                self.audio_queue.task_done()
    
    def start_listening(self):
        self.recognize_thread = Thread(target=self.recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()
        print("Starting")
        with sr.Microphone() as source:
            try:
                while True:
                    audio = self.r.listen(source)
                    with self.audio_queue_lock:
                        self.audio_queue.put(audio)
            except KeyboardInterrupt:
                pass

        with self.audio_queue_lock:
            self.audio_queue.join()
            self.audio_queue.put(None)
        self.recognize_thread.join()

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    recognizer.start_listening()
