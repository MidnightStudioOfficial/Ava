""" AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()

Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md

"""
import sys
import time
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

class AnimatedGif(ctk.CTkLabel):
	"""
	Class to show animated GIF file in a label
	Use start() method to begin animation, and set the stop flag to stop it
	"""
	def __init__(self, root, gif_file, delay=0.04):
		"""
		:param root: tk.parent
		:param gif_file: filename (and path) of animated gif
		:param delay: delay between frames in the gif animation (float)
		"""
		ctk.CTkLabel.__init__(self, root)
		self.root = root
		self.gif_file = gif_file
		self.delay = delay  # Animation delay - try low floats, like 0.04 (depends on the gif in question)
		self.stop = False  # Thread exit request flag

		self._num = 0

	def start(self):
		"""Starts non-threaded version that we need to manually update()"""
		self.start_time = time.perf_counter()  # Starting timer
		self._animate()

	def stop(self):
		"""This stops the after loop that runs the animation, if we are using the after() approach"""
		self.stop = True

	def _animate(self):
		try:
			self.gif = ImageTk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # Looping through the frames
			self.configure(image=self.gif)
			self._num += 1
		except tk.TclError:  # When we try a frame that doesn't exist, we know we have to start over from zero
			self._num = 0
		if not self.stop:    # If the stop flag is set, we don't repeat
			self.root.after(int(100), self._animate)

	def start_thread(self):
		"""This starts the thread that runs the animation, if we are using a threaded approach"""
		from threading import Thread  # We only import the module if we need it
		#self._animation_thread = Thread(daemon=True)
		self._animation_thread = Thread(target=self._animate_thread,daemon=True).start()  # Forks a thread for the animation

	def stop_thread(self):
		"""This stops the thread that runs the animation, if we are using a threaded approach"""
		self.stop = True

	def _animate_thread(self):
		"""Updates animation, if it is running as a separate thread"""
		while self.stop is False:  # Normally this would block mainloop(), but not here, as this runs in separate thread
			try:
				time.sleep(self.delay)
				self.gif = ImageTk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # Looping through the frames
				self.configure(image=self.gif)
				self._num += 1
			except tk.TclError:  # When we try a frame that doesn't exist, we know we have to start over from zero
				self._num = 0
			except RuntimeError:
				sys.exit()


if __name__ == '__main__':
 root = ctk.CTk()
 f = ctk.CTkFrame(root)
 f.pack()
 l = ctk.CTkLabel(f)
 l.pack()
 lbl_with_my_gif = AnimatedGif(f, 'Data/ai2.gif', 0.001)  # (tkinter.parent, filename, delay between frames)
 lbl_with_my_gif.pack()  # Packing the label with the animated gif (grid works just as well)
 lbl_with_my_gif.start_thread()  # Spawn thread which updates animation
 root.mainloop()
 lbl_with_my_gif.stop_thread()  # Setting stop flag, which ends the animation
