import pyaudio
import threading
import wave

#ffmpeg -i song.mp3 -acodec pcm_u8 -ar 22050 song.wav


class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.playing = False
        self.thread = None

    def play(self):
        if self.playing:
            print("Audio is already playing.")
            return

        self.playing = True
        self.thread = threading.Thread(target=self.play_audio, daemon=True)
        self.thread.start()

    def set_file(self, new_filename):
        if self.playing:
            print("Audio is already playing. Cant set new filename")
            return
        self.filename = new_filename

    def process_audio(self):
        pass

    def play_audio(self):
        chunk = 1024
        wf = wave.open(self.filename, 'rb')

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(chunk)

        while data: # and self.playing
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        self.playing = False

    def stop(self):
        if not self.playing:
            print("Audio is not playing.")
            return

        self.playing = False
        self.thread.join()


# # Usage example
# player = AudioPlayer("audio.wav")
# player.play()

# # Do some other work while audio is playing

# # Stop audio playback
# player.stop()
