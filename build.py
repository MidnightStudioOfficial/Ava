import os
import shutil

#os.system("pyinstaller --collect-all chatterbot --distpath ./bin ./src/main.py")

#shutil.copy("BuildData/customtkinter", "bin/main")
os.mkdir("bin/main/customtkinter")
os.system("xcopy BuildData\customtkinter bin\main /e /i")
#print(os.path.dirname("BuildData/customtkinter"))
#os.system("xcopy BuildData\customtkinter bin\main /e /i")