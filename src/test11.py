import os
import psutil
import time
import matplotlib.pyplot as plt

def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

memory = []
times = []

start_time = time.time()

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(times, memory)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Memory Usage (MB)')

while True:
    memory.append(memory_usage())
    times.append(time.time() - start_time)
    line.set_xdata(times)
    line.set_ydata(memory)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(2)

plt.show()
