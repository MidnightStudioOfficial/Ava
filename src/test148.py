import customtkinter as CTk
import tkinter as tk
from PIL import Image, ImageTk
import os
import PIL.Image
import PIL.ImageTk

images = [
    Image.open("Data/assets/bell.png"),
    Image.open("Data/assets/box.png")
]

# Create the main window
root = CTk.CTk()
root.title("Image Slideshow")
root.geometry("600x400")

# Create a frame to hold the images
frame = CTk.CTkFrame(root)
frame.pack(expand=True, fill="both")

# Create a label to display the current image
label = CTk.CTkLabel(frame)
label.pack(expand=True, fill="both")

# Create a slider to control the slideshow
slider = CTk.CTkSlider(frame, from_=0, to=len(images) - 1)
slider.pack(side="bottom")

# Update the label and slider every second
def update():
    global index
    index = int(slider.get())
    if index < len(images):
        photo = ImageTk.PhotoImage(images[index])
        label.configure(image=photo)
        slider.set(index + 1)

    root.after(1000, update)



# Start the slideshow
update()

root.mainloop()
