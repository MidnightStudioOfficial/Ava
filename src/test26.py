import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Sample format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)
FRAME_RATE = 30  # Frame rate (Hz)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Create a figure and axis for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Initialize the line data
x = np.linspace(0, CHUNK, CHUNK)
y = np.zeros(CHUNK)

# Update function for animation
def update(frame):
    # Read audio samples from the stream
    data = stream.read(CHUNK)
    audio = np.frombuffer(data, dtype=np.int16)

    # Update the line data
    line.set_data(x, audio)

    return line

# Set up the plot
ax.set_xlim(0, CHUNK)
ax.set_ylim(-32768, 32768)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=FRAME_RATE, blit=True)

# Show the plot
plt.show()

# Clean up resources
stream.stop_stream()
stream.close()
p.terminate()
