from core.AudioStream.output import AudioPlayer



# import wave
# import sys

# import pyaudio

# CHUNK = 1024

# with wave.open("Data/rosie2.wav", 'rb') as wf:
#     # Instantiate PyAudio and initialize PortAudio system resources (1)
#     p = pyaudio.PyAudio()

#     # Open stream (2)
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)

#     # Play samples from the wave file (3)
#     while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
#         stream.write(data)

#     # Close stream (4)
#     stream.close()

#     # Release PortAudio system resources (5)
#     p.terminate()
if __name__ == '__main__':
 a = AudioPlayer("./Data/rosie2.wav")
 a.play()
 