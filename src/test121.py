from queue import Queue, Empty
from threading import Thread, Condition
import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, wake_words=("ava", "eva", "hangover"), callback_function=None):
        self.wake_words = wake_words
        self.r = sr.Recognizer()
        self.words_queue = []
        self.audio_queue = Queue()
        self.callback = callback_function
        self.condition = Condition()  # Condition for synchronization

    def check_for_wakeword(self, text):
        if any(wake_word in text for wake_word in self.wake_words):
            print("I can hear you")
            self.callback(text)

    def recognize_worker(self):
        # This runs in a background thread
        while True:
            with self.condition:
                self.condition.wait(timeout=1)  # Wait for signal or timeout
                if self.audio_queue.empty():
                    continue

            audio_chunks = []
            try:
                while True:
                    audio = self.audio_queue.get_nowait()
                    if audio is None:
                        break  # Stop processing if the main thread is done
                    audio_chunks.append(audio)
            except Empty:
                pass

            # Batch audio chunks and process them together
            if audio_chunks:
                audio_batch = sr.AudioData(b''.join(audio_chunks), self.r.SAMPLE_RATE, self.r.SAMPLE_WIDTH)
                try:
                    text = self.r.recognize_google(audio_batch)
                    self.check_for_wakeword(text.lower())
                    print("Recognized speech: " + str(text))
                    self.words_queue.append(text)
                except sr.UnknownValueError:
                    print("Speech recognition could not understand audio")
                except sr.RequestError as e:
                    print("Error requesting results from the recognition service: {0}".format(e))

    def _start_listening(self):
        # Start a new thread to recognize audio while this thread focuses on listening
        self.recognize_thread = Thread(target=self.recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()
        print("Starting")
        with sr.Microphone() as source:
            try:
                while True:
                    with self.condition:
                        audio = self.r.listen(source)
                        self.audio_queue.put(audio)
                        self.condition.notify_all()  # Notify the worker thread
            except KeyboardInterrupt:  # Allow Ctrl + C to shut down the program gracefully
                pass

            self.audio_queue.put(None)  # Tell the recognize_thread to stop
            self.recognize_thread.join()  # Wait for the recognize_thread to actually stop

    def stop_listening(self):
        self.condition.acquire()
        self.audio_queue.put(None)
        self.condition.notify_all()
        self.condition.release()

    def start_listening(self):
        self._start_listening()


if __name__ == "__main__":
    def callback_function(text):
        print("Callback triggered with text:", text)

    recognizer = SpeechRecognizer(wake_words=("ava", "eva", "hangover"), callback_function=callback_function)
    recognizer.start_listening()
