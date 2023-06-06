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