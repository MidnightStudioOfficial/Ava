import customtkinter as CTk
import os
import PIL.Image
import PIL.ImageTk

def load_images(directory):
  """Loads all the images in the specified directory."""
  images = []
  for filename in os.listdir(directory):
    path = os.path.join(directory, filename)
    image = PIL.Image.open(path)
    image = image.resize((200, 200))
    image = PIL.ImageTk.PhotoImage(image)
    images.append(image)
  return images

def show_image(image, label):
  """Shows the specified image in the label."""
  label.configure(image=image)

def next_image(index):
  """Shows the next image in the slideshow."""
  global image_index
  image_index = (image_index + 1) % len(images)
  show_image(images[image_index], image_label)

def previous_image(index):
  """Shows the previous image in the slideshow."""
  global image_index
  image_index = (image_index - 1) % len(images)
  show_image(images[image_index], image_label)

def start_slideshow():
  """Starts the slideshow."""
  global timer
  timer = CTk.Timer(interval=2000, callback=next_image)
  timer.start()

root = CTk.CTk()
root.title("Image Slideshow")

images = load_images("Data/assets")
image_index = 0

image_label = CTk.CTkLabel(root)
show_image(images[image_index], image_label)

next_button = CTk.CTkButton(root, text="Next", command=lambda: next_image(image_index))
previous_button = CTk.CTkButton(root, text="Previous", command=lambda: previous_image(image_index))

next_button.pack()
previous_button.pack()
image_label.pack()

#start_slideshow()

root.mainloop()
