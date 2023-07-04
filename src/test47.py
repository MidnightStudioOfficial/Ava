from tqdm.tk import tqdm
from tkinter import Tk, Label
import time
import os

root = Tk()
label = Label(root)
label.pack()

file_path = 'CTkTheme_test.json'
corpus = [1, 2, 3, 4, 5]

def task():
    prog = tqdm(total=len(corpus), desc='Training ' + str(os.path.basename(file_path)), gui=True)
    for conversation_count, conversation in enumerate(corpus):
        prog.set_description_str("{} {} {} {:.3}%".format('Training ' + str(os.path.basename(file_path)),
                        conversation_count + 1,
                        len(corpus), (conversation_count + 1) * 100.0 / len(corpus)))
        prog.update()
        time.sleep(1)

label.after(0, task)
root.mainloop()
