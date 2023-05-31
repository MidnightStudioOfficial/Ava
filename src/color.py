import tkinter as tk

# Create a window
root = tk.Tk()

# Create a canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Define the colors for the gradient
color1 = "#ff0000"
color2 = "#00ff60"
color3 = "#0000ff"

# Create a rectangle with a gradient
for i in range(400):
    color = '#{:02x}{:02x}{:02x}'.format(
        int((i/400)*int(color1[1:3], 16) + ((400-i)/400)*int(color2[1:3], 16)),
        int((i/400)*int(color1[3:5], 16) + ((400-i)/400)*int(color2[3:5], 16)),
        int((i/400)*int(color1[5:7], 16) + ((400-i)/400)*int(color2[5:7], 16))
    )
    canvas.create_rectangle(0, i, 400, i+1, fill=color)

for i in range(400):
    color = '#{:02x}{:02x}{:02x}'.format(
        int((i/400)*int(color2[1:3], 16) + ((400-i)/400)*int(color3[1:3], 16)),
        int((i/400)*int(color2[3:5], 16) + ((400-i)/400)*int(color3[3:5], 16)),
        int((i/400)*int(color2[5:7], 16) + ((400-i)/400)*int(color3[5:7], 16))
    )
    canvas.create_rectangle(0, i+200, 400, i+201, fill=color)

# Start the main loop
root.mainloop()
