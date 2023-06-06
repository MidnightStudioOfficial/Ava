def install_and_import(package_name, I_Name, pack):
        import importlib
        print(str(I_Name))
        print("Importing packages")
        globals()[package_name] = importlib.import_module(package_name, package=pack)
        

import threading

t1 = threading.Thread(target=install_and_import, args=("pandas","read_csv", "read_csv"))
t1.start()
t1.join()
df = pandas.read_csv("Data/articulations.csv")
print(df)
import spacy
spacy