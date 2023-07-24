import threading

class Importer:
    def __init__(self, modules) -> None:
        self.modules = modules
        self.threads = []

    def import_module2(self, package_name, pack):
        import importlib
        print("Importing "+str(package_name))
        globals()[package_name] = importlib.import_module(package_name, package=pack)

    def import_all(self):
        for n in self.modules:
          t = threading.Thread(target=self.import_module2, args=(self.modules[n]["package_name"], self.modules[n]["pack"]))
          self.threads.append(t)
          t.start()
        # wait for the threads to complete
        for t in self.threads:
            t.join()
