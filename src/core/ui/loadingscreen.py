from customtkinter import CTkLabel, CTkProgressBar, CTkToplevel, CTkButton

class SplashScreen(CTkToplevel):
    def __init__(self, parent):
        """
        Initialize the SplashScreen class.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.parent = parent
        self.title("Splash Screen")
        self.geometry("300x200")
        self.configure(background="#2c3e50")

        # Create the widgets
        self.text_label = CTkLabel(self, text="Loading...", font=("Arial", 16))
        self.text_label.pack(pady=(50, 10))

        self.progressbar = CTkProgressBar(
            self,
            orientation="horizontal",
            mode="determinate",
            width=250
        )
        self.progressbar.pack(pady=10)

        self.cancel_button = CTkButton(self, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=10)

        # Center the window on the screen
        # Update the window to process any pending events and ensure it's up to date before proceeding.
        self.update_idletasks()

        # Get the current width and height of the window.
        width = self.winfo_width()
        height = self.winfo_height()

        # Calculate the X and Y coordinates to center the window on the screen.
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        # Set the window's position to be centered on the screen.
        self.geometry(f"+{x}+{y}")

    def set_text(self, text):
        """
        Update the text label on the SplashScreen.

        Args:
            text (str): The new text to display.
        """
        self.text_label.configure(text=text)
        self.update()

    def set_progress(self, value):
        """
        Set the progress value for the progress bar.

        Args:
            value (int): The new progress value (0-100).
        """
        try:
            for _ in range(value):
                self.progressbar.step()
            self.update()
        except Exception as e:
            # Add code here to handle the error
            print("Error:" + str(e))

    def cancel(self):
        """Handle the cancel button click event."""
        self.parent.destroy()
