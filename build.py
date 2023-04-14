import os

os.system("pyinstaller --collect-all chatterbot --distpath ./bin ./src/main.py")