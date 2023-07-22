import threading

def install_and_import(package_name, pack):
        import importlib
        print(str(package_name))
        print("Importing packages")
        globals()[package_name] = importlib.import_module(package_name, package=pack)

modules = {
    "Engine": {
        "package_name": "core.engine.Engine",
        "pack": "ConversationalEngine"     
    },
    "Conversation": {
        "package_name": "core.engine.Conversation",
        "pack": "Conversation"     
    },
    "spacy": {
        "package_name": "spacy",
        "pack": "load"     
    }
}

threads = []
for n in modules:
    t = threading.Thread(target=install_and_import, args=(modules[n]["package_name"],modules[n]["pack"]))
    threads.append(t)
    t.start()

# wait for the threads to complete
for t in threads:
    t.join()

print("DONE")

class Importer:
    def __init__(self, modules) -> None:
        self.modules = modules
        self.threads = []

    def import_module(self, package_name, pack):
        import importlib
        print("Importing "+str(package_name))
        globals()[package_name] = importlib.import_module(package_name, package=pack)
    def import_all(self):
        for n in self.modules:
          t = threading.Thread(target=self.import_module, args=(self.modules[n]["package_name"], self.modules[n]["pack"]))
          self.threads.append(t)
          t.start()
