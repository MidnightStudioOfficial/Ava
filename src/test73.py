import tkinter as tk
from PIL import Image, ImageTk
import threading

class ImageLabel(tk.Label):
    """A label that displays images and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        self.image = None

        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                if len(self.frames) == 1:
                    self.config(image=self.frames[0])
                self.loc += 1
                im.seek(self.loc)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) > 1:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.image = None
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

def load_image(label, image_path):
    im = Image.open(image_path)
    label.load(im)

def main():
    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack()

    image_path = "Data/ai2.gif"  # enter your file location here

    thread = threading.Thread(target=load_image, args=(lbl, image_path))
    thread.daemon = True
    thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
