import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CHUNK = 1024  # Number of audio samples per frame
BUFFER_SIZE = 2  # Number of frames to accumulate before updating plot 10
FORMAT = pyaudio.paInt16  # Sample format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (Hz)
FRAME_RATE = 60  # Frame rate (Hz) 30

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Create a Tkinter window
root = tk.Tk()
root.title("Audio Visualizer")

# Create a frame for the plot
frame = tk.Frame(root)
frame.pack()

# Create a label
label = tk.Label(frame, text="Audio Visualizer", font=("Helvetica", 16))
label.pack(pady=10)

# Create a figure and axis for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Initialize the line data
x = np.linspace(0, CHUNK, CHUNK)
y = np.zeros(CHUNK)

# Initialize the buffer
buffer = np.zeros((BUFFER_SIZE, CHUNK))

# Update function for animation
def update(frame):
    # Read audio samples from the stream
    for i in range(BUFFER_SIZE):
        data = stream.read(CHUNK)
        audio = np.frombuffer(data, dtype=np.int16)
        buffer[i] = audio

    # Calculate the average audio from the buffer
    average_audio = np.mean(buffer, axis=0)

    # Update the line data
    line.set_data(x, average_audio)

    return line,

# Set up the plot
ax.set_xlim(0, CHUNK)
ax.set_ylim(-32768, 32768)
ax.axis('off')

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=FRAME_RATE, blit=True)

# Embed the plot into the Tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Create a button
button = tk.Button(frame, text="Exit", command=root.quit)
button.pack(pady=10)

def on_closing():
    stream.stop_stream()
    stream.close()
    p.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()

# Clean up resources
stream.stop_stream()
stream.close()
p.terminate()
