import os
import shutil

#os.system("pyinstaller --collect-all comtypes --collect-all blis --collect-all pywin32_system32 --collect-all win32comext --collect-all spacy --collect-all sklearn --collect-all win32com --collect-all win32ctypes --distpath ./bin ./src/main.py")
os.system("pyinstaller --distpath ./bin main.spec")
#shutil.copy("BuildData/customtkinter", "bin/main")

# Create bin dirs
os.mkdir("bin/main/customtkinter")
os.mkdir("bin/main/en_core_web_sm")
#os.mkdir("bin/main/assets")
#os.mkdir("bin/main/training")
os.mkdir("bin/main/Data")

# Copying all the files
os.system("xcopy BuildData\customtkinter bin\main\customtkinter /e /i")
os.system("xcopy BuildData\en_core_web_sm bin\main\en_core_web_sm /e /i")
#os.system("xcopy BuildData\assets bin\main\assets /e /i")
#os.system("xcopy BuildData\training bin\main\training /e /i")
os.system("xcopy BuildData\Data bin\main\Data /e /i")

#print(os.path.dirname("BuildData/customtkinter"))
#os.system("xcopy BuildData\customtkinter bin\main /e /i")
