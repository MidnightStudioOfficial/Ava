from core.engine.EngineCore.engine import MainEngine

e = MainEngine()
print(e.getIntent("can you tell me a joke"))
print(e.getIntent("can you you play some music"))
print(e.getIntent("can you tell me what the weather is today"))
print(e.getIntent("hey how are you"))
print(e.getIntent("google search for what is python programming"))
print(e.getIntent("wikipedia search for cats"))

while True:
    print(e.getIntent(input(">>>")))
