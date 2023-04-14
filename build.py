import os
import shutil

os.system("pyinstaller --collect-all chatterbot --distpath ./bin ./src/main.py")

#shutil.copy("BuildData/customtkinter", "bin/main")

# Create bin dirs
os.mkdir("bin/main/customtkinter")
os.mkdir("bin/main/assets")
os.mkdir("bin/main/training")

# Copying all the files
os.system("xcopy BuildData\customtkinter bin\main\customtkinter /e /i")
os.system("xcopy BuildData\assets bin\main\assets /e /i")
os.system("xcopy BuildData\training bin/main/training /e /i")


#print(os.path.dirname("BuildData/customtkinter"))
#os.system("xcopy BuildData\customtkinter bin\main /e /i")