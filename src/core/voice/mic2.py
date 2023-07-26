from queue import Queue
from threading import Thread, Event
import speech_recognition as sr


class SpeechRecognizer:
    def __init__(self, wake_words=("ava", "eva", "hangover"), callback_function=None):
        self.wake_words = wake_words
        self.r = sr.Recognizer()
        self.words_queue = []
        self.audio_queue = Queue()
        self.callback = callback_function
        self.stop_event = Event()  # Event to signal when to stop listening

    def check_for_wakeword(self, text):
        if any(wake_word in text for wake_word in self.wake_words):
            print("I can hear you")
            self.callback(text)

    def recognize_worker(self):
        # This runs in a background thread
        while not self.stop_event.is_set():
            try:
                audio = self.audio_queue.get(timeout=1)  # Wait for 1 second for audio data
                if audio is None:
                    break  # Stop processing if the main thread is done

                # Received audio data, now we'll recognize it using Google Speech Recognition
                try:
                    text = self.r.recognize_google(audio)
                    self.check_for_wakeword(text.lower())
                    print("Google Speech Recognition thinks you said: " + str(text))
                    self.words_queue.append(text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service: {0}".format(e))

            except Queue.Empty:
                pass  # If no audio is available, continue looping

            self.audio_queue.task_done()  # Mark the audio processing job as completed in the queue

    def _start_listening(self):
        # Start a new thread to recognize audio while this thread focuses on listening
        self.recognize_thread = Thread(target=self.recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()
        print("Starting")
        with sr.Microphone() as source:
            try:
                while not self.stop_event.is_set():
                    # Repeatedly listen for phrases and put the resulting audio on the audio processing job queue
                    self.audio_queue.put(self.r.listen(source))
            except KeyboardInterrupt:  # Allow Ctrl + C to shut down the program gracefully
                self.stop_event.set()

        self.audio_queue.join()  # Block until all current audio processing jobs are done
        self.audio_queue.put(None)  # Tell the recognize_thread to stop
        self.recognize_thread.join()  # Wait for the recognize_thread to actually stop

    def stop_listening(self):
        self.stop_event.set()

    def start_listening(self):
        self.stop_event.clear()
        self._start_listening()


if __name__ == "__main__":
    def callback_function(text):
        print("Callback triggered with text:", text)

    recognizer = SpeechRecognizer(callback_function=callback_function)
    recognizer.start_listening()
