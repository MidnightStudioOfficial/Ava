import tkinter as tk
import pyaudio
import numpy as np
import random

# Constants for audio processing
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# Create the Tkinter application window
window = tk.Tk()
window.title("Multi-Frequency Waves")
canvas = tk.Canvas(window, width=800, height=400, bg="white")
canvas.pack()

# Function to generate random color
def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# Generate colors for each wave
num_waves = 2
wave_colors = [random_color() for _ in range(num_waves)]

# Function to draw the voice waves on the canvas
def draw_waves(wave_data):
    canvas.delete("wave")  # Clear previous waves
    num_samples = len(wave_data[0])
    x_scale = 800 / num_samples
    x = 0
    for i, wave in enumerate(wave_data):
        points = []
        for j in range(0, num_samples):
            y = 200 + wave[j] * 100  # Adjust amplitude and vertical position
            points.extend([x, y])
            x += x_scale
        color = wave_colors[i % num_waves]  # Cycle through the wave colors
        canvas.create_line(points, fill=color, width=2, tags="wave")

# Function to read audio data and update the canvas
def update_canvas(stream):
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        wave_data = np.frombuffer(data, dtype=np.int16).reshape(-1, CHUNK) / 32768.0  # Normalize wave data
        draw_waves(wave_data)
    except Exception as e:
        print("Error:", str(e))

# Set up PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Start the Tkinter event loop
def update():
    update_canvas(stream)
    window.after(70, update) #10

update()  # Start the update loop
window.mainloop()

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
