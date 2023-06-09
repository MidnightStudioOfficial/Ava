import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Constants
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
x = np.arange(0, CHUNK_SIZE//2, 1)
line, = ax.plot(x, np.zeros(CHUNK_SIZE//2), color='lightblue', lw=6)

# Function to update the plot
def update_plot(frame):
    # Read audio data from the stream
    audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.float32)

    # Compute the power spectrum
    power_spectrum = np.abs(np.fft.fft(audio_data))[:CHUNK_SIZE//2]

    # Update the line data
    line.set_ydata(power_spectrum)

    return line,

# Set up the animation
ani = animation.FuncAnimation(fig, update_plot, interval=0)

# Customize the plot
ax.set_facecolor('black')
ax.set_ylim(0, 1000)  # Adjust the y-axis limit as needed
ax.set_xlim(0, CHUNK_SIZE//2)
ax.axis('off')

ax.set_aspect(4) #4

# Create a Tkinter window
root = tk.Tk()
root.title("Audio Visualizer")

# Create a FigureCanvasTkAgg instance
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Close the stream and terminate PyAudio when the window is closed
def on_closing():
    stream.stop_stream()
    stream.close()
    p.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
tk.mainloop()
