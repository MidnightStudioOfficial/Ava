from core.windows.control import Control

c = Control()
c.open_app(app="settings")
#c.change_volume(40)
# import ctypes

# class WindowsController:
#     def __init__(self):
#         self.user32 = ctypes.windll.user32


#     def set_wallpaper(self, path):
#         SPI_SETDESKWALLPAPER = 20
#         self.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

#     def message_box(self, text, title):
#         MB_OK = 0
#         self.user32.MessageBoxW(0, text, title, MB_OK)

# controller = WindowsController()
# controller.set_wallpaper(r'C:\path\to\wallpaper.jpg')
# controller.message_box('Hello', 'Message Box')
