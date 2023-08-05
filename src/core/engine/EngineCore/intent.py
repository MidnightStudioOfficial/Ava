class IntentHandler:
    def __init__(self):
        self.intents = {}

    def add_intent(self, intent_name, action_function):
        self.intents[intent_name] = action_function

    def process_intent(self, intent_name, *args, **kwargs):
        if intent_name in self.intents:
            return self.intents[intent_name](*args, **kwargs)
        else:
            return "Intent not recognized."

def greet(name):
    return f"Hello, {name}!"

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    intent_handler = IntentHandler()
    intent_handler.add_intent("greet", greet)
    intent_handler.add_intent("add_numbers", add_numbers)

    while True:
        user_input = input("Enter intent: ")
        if user_input == "exit":
            break

        if " " in user_input:
            intent, *args = user_input.split()
            result = intent_handler.process_intent(intent, *map(float, args))
        else:
            result = intent_handler.process_intent(user_input)

        print(result)