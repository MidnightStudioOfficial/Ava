import threading
import random

thoughts = ["I wonder what the weather is like today", "I should call my friend", "What should I have for dinner?", "I need to finish that project", "I want to go on a vacation"]
rules = {
    "weather": ["It might rain today", "It's going to be sunny", "I hope it doesn't snow"],
    "friend": ["I miss talking to them", "We should catch up", "I wonder how they're doing"],
    "dinner": ["Maybe I'll cook something", "I could order takeout", "I feel like eating something healthy"],
    "project": ["I need to focus and get it done", "It's almost finished", "I'm making good progress"],
    "vacation": ["I want to go somewhere warm", "I need a break from work", "It would be nice to explore a new place"]
}

def generate_random_thought():
    thought = random.choice(thoughts)
    if thought == thoughts[0]:
        return thought + ". " + random.choice(rules["weather"])
    elif thought == thoughts[1]:
        return thought + ". " + random.choice(rules["friend"])
    elif thought == thoughts[2]:
        return thought + ". " + random.choice(rules["dinner"])
    elif thought == thoughts[3]:
        return thought + ". " + random.choice(rules["project"])
    else:
        return thought + ". " + random.choice(rules["vacation"])

def add_thought(thought):
    thoughts.append(thought)

def add_rule(category, rule):
    if category in rules:
        rules[category].append(rule)
    else:
        rules[category] = [rule]

#print(generate_random_thought())

add_thought("I need to exercise more")
add_rule("exercise", "I should go for a run")
add_rule("exercise", "I could do some yoga")


stop = False


def my_function():
    # Your code here
    print(generate_random_thought())

def run_every_3_minutes():
    global stop
    if not stop:
        my_function()
        threading.Timer(6, run_every_3_minutes).start() #180

# Start the repeating function in a separate thread
thread = threading.Thread(target=run_every_3_minutes)
thread.start()

# Your main program code here
while True:
    # Your code here
    #print("Main program running")
    # Set stop to True to stop the repeating function
    #stop = True
    pass
