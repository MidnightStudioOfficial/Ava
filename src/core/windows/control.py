import subprocess
import sys
from ctypes import WinDLL

class Control:
    def __init__(self):
        pass

    def open_app(self, app):
        try:
            if sys.platform.startswith("win"):
                if app == "settings":
                    # Open Windows Settings
                    subprocess.run("explorer ms-settings:", shell=True)
                elif app == "calculator":
                    # Open Windows Calculator
                    subprocess.run("calc.exe", shell=True)
                elif app == "notepad":
                    # Open Windows Notepad
                    subprocess.run("notepad.exe", shell=True)
                elif app == "paint":
                    # Open Windows Paint
                    subprocess.run("mspaint.exe", shell=True)
                else:
                    raise ValueError("Unsupported application: " + app)

                return True  # Indicate successful operation
            else:
                print("Unsupported operating system. Only Windows is supported.")

        except subprocess.SubprocessError as e:
            print("Error opening the application:", str(e))
        except Exception as e:
            print("Error opening the application:", str(e))

        return False  # Indicate failure

    def change_volume(self, volume: int):
        """
        Change the system volume in Windows.

        :param volume: The desired change in volume, as an integer. Positive values increase the volume, while negative values decrease it.
        """
        try:
            if sys.platform.startswith("win"):
                user32 = WinDLL("user32")
                # Key codes for volume up and volume down
                VOLUME_UP_KEY = 0xAF
                VOLUME_DOWN_KEY = 0xAE

                if volume > 0:
                    key = VOLUME_UP_KEY
                else:
                    key = VOLUME_DOWN_KEY
                    volume = abs(volume)

                for _ in range(volume):
                    # Simulate key press and release for changing volume
                    user32.keybd_event(key, 0, 0, 0)  # Key press
                    user32.keybd_event(key, 0, 2, 0)  # Key release

                return True  # Indicate successful operation
            else:
                print("Unsupported operating system. Only Windows is supported.")

        except OSError as e:
            print("OS Error:", str(e))
        except ValueError as e:
            print("Value Error:", str(e))
        except Exception as e:
            print("Error changing the volume:", str(e))

        return False  # Indicate failure
