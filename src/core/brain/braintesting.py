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

print(generate_random_thought())

add_thought("I need to exercise more")
add_rule("exercise", "I should go for a run")
add_rule("exercise", "I could do some yoga")

print(generate_random_thought())

import random

templates = [
    "I wonder if {weather}. Maybe I should {activity}.",
    "I haven't talked to {friend} in a while. I wonder if they would like to {activity}.",
    "I'm not sure what to have for dinner. Maybe I'll {activity}.",
    "I need to finish that project. I should {activity}.",
    "I want to go on a vacation. It would be nice to {activity}."
]
rules = {
    "weather": ["it will rain today", "it will be sunny", "it will snow"],
    "friend": ["Alice", "Bob", "Charlie"],
    "activity": ["go for a walk", "read a book", "watch a movie"]
}

def generate_random_sentence():
    template = random.choice(templates)
    sentence = template.format(
        weather=random.choice(rules["weather"]),
        friend=random.choice(rules["friend"]),
        activity=random.choice(rules["activity"])
    )
    return sentence

print(generate_random_sentence())


import random

thoughts = {
    "happy": ["I wonder what the weather is like today", "I should call my friend", "What should I have for dinner?"],
    "sad": ["I need to finish that project", "I want to go on a vacation"]
}
rules = {
    "weather": ["It might rain today", "It's going to be sunny", "I hope it doesn't snow"],
    "friend": ["I miss talking to them", "We should catch up", "I wonder how they're doing"],
    "dinner": ["Maybe I'll cook something", "I could order takeout", "I feel like eating something healthy"],
    "project": ["I need to focus and get it done", "It's almost finished", "I'm making good progress"],
    "vacation": ["I want to go somewhere warm", "I need a break from work", "It would be nice to explore a new place"]
}

def generate_thought(mood):
    thought = random.choice(thoughts[mood])
    if thought == thoughts[mood][0]:
        return thought + ". " + random.choice(rules["weather"])
    elif thought == thoughts[mood][1]:
        return thought + ". " + random.choice(rules["friend"])
    elif thought == thoughts[mood][2]:
        return thought + ". " + random.choice(rules["dinner"])
    elif thought == thoughts[mood][3]:
        return thought + ". " + random.choice(rules["project"])
    else:
        return thought + ". " + random.choice(rules["vacation"])

def add_thought(mood, thought):
    if mood in thoughts:
        thoughts[mood].append(thought)
    else:
        thoughts[mood] = [thought]

def add_rule(category, rule):
    if category in rules:
        rules[category].append(rule)
    else:
        rules[category] = [rule]

print(generate_thought("happy"))

add_thought("happy", "I need to exercise more")
add_rule("exercise", "I should go for a run")
add_rule("exercise", "I could do some yoga")

print(generate_thought("happy"))


class Person:
    def __init__(self, name, traits):
        self.name = name
        self.traits = traits
        self.mood = 0.0

    def update_mood(self):
        for trait in self.traits:
            if trait == 'happy':
                self.mood += 0.1
            elif trait == 'sad':
                self.mood -= 0.1
            elif trait == 'angry':
                self.mood -= 0.2
            elif trait == 'calm':
                self.mood += 0.2

p1 = Person('Alice', ['happy', 'calm'])
p1.update_mood()
print(p1.name + "'s mood: " + str(p1.mood))

p2 = Person('Bob', ['sad', 'angry'])
p2.update_mood()
print(p2.name + "'s mood: " + str(p2.mood))
