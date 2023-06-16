import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Constants
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024
BAR_WIDTH = 0.8

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# Create the figure and axis
fig, ax = plt.subplots()
x = np.arange(0, CHUNK_SIZE, 1)
bar_container = ax.bar(x, np.zeros(CHUNK_SIZE), BAR_WIDTH)

# Update function for the animation
def update_plot(frame):
    # Read audio data from the stream
    audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.float32)

    # Compute the power spectrum
    power_spectrum = np.abs(np.fft.fft(audio_data))[:CHUNK_SIZE//2]

    # Update the bar heights
    for bar, height in zip(bar_container, power_spectrum):
        bar.set_height(height)

    return bar_container

# Set up the animation
ani = animation.FuncAnimation(fig, update_plot, interval=0)

# Show the plot
plt.show()

# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
