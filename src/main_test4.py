"""
  Author: MidnightStudioOfficial
  License: MIT
  Description: This is the main script that loads and connects everything
"""
from core.ui.ui2 import ChatBotGUI
import customtkinter as ctk
from os.path import join, dirname, realpath

print("Importing loadingscreen")
from core.ui.loadingscreen2 import SplashScreen

if __name__ == '__main__':


    """
    Main entry point of the program.
    This script creates a GUI for the Ava Chatbot application with a splash screen that shows a loading progress.
    """
    image_path = join(dirname(realpath(__file__)), "Data/assets")
    

    print('Creating GUI')

    # Create the root window
    root = ctk.CTk()

    # Create and configure the splash screen
    splash_screen = SplashScreen(root)
    splash_screen.overrideredirect(True)
    splash_screen.set_text("Creating Ava Chatbot and training")
    splash_screen.set_progress(50)

    print('Creating Ava Chatbot and training')

    # Create the ChatBotGUI object
    gui = ChatBotGUI(root, splash_screen, image_path)

    # Update the splash screen
    splash_screen.set_text("Done")
    splash_screen.set_progress(100)

    # Destroy the splash screen
    splash_screen.destroy()

    # Start the main event loop
    root.mainloop()
