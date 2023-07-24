# Author: MidnightStudioOfficial
# License: MIT
# Description: This script can sumulate a human brain

import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import random
import threading

stop = False

class Traits:
    def __init__(self) -> None:
       self.traits_available = {
           "depression": {
               "mood_score": -0.5
           }
       }

class Brain:
    def __init__(self):
        # Initialize mood to 0.0 and create an empty list for mood history
        self.mood = 0.0
        self.mood_history = []

        self.thought = ""
        self.thoughts = {
        "happy": ["I wonder what the weather is like today", "I should call my friend", "What should I have for dinner?"],
        "sad": ["I need to finish that project", "I want to go on a vacation"]
        }
        self.rules = {
        "weather": ["It might rain today", "It's going to be sunny", "I hope it doesn't snow"],
        "friend": ["I miss talking to them", "We should catch up", "I wonder how they're doing"],
        "dinner": ["Maybe I'll cook something", "I could order takeout", "I feel like eating something healthy"],
        "project": ["I need to focus and get it done", "It's almost finished", "I'm making good progress"],
        "vacation": ["I want to go somewhere warm", "I need a break from work", "It would be nice to explore a new place"]
        }
        self.traits = []
        self.memory = {}

        # Create an instance of the SentimentIntensityAnalyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def update_mood(self, text):
        # Get the sentiment scores for the given text
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        # Get the compound score from the sentiment scores
        sentiment_score = sentiment_scores["compound"]
        # Update the mood by adding the sentiment score
        self.mood += sentiment_score
        # Append the current mood to the mood history list
        self.mood_history.append(self.mood)

    def get_mood(self):
        # Return the current mood
        return self.mood

    def reset_mood(self):
        # Reset the mood to 0.0 and clear the mood history list
        self.mood = 0.0
        self.mood_history = []

    def mood_as_string(self):
        # Return a string representation of the current mood based on its value
        if self.mood > 0.5:
            return "Very happy"
        elif self.mood > 0:
            return "Happy"
        elif self.mood == 0:
            return "Neutral"
        elif self.mood > -0.5:
            return "Sad"
        else:
            return "Very sad"

    def get_mood_history(self):
        # Return the mood history list
        return self.mood_history

    def plot_mood_history(self):
        # Plot the mood history using matplotlib
        plt.plot(self.mood_history)
        plt.title("Mood History")
        plt.xlabel("Time")
        plt.ylabel("Mood")
        plt.show()

    def add_thought(self, mood, thought):
     if mood in self.thoughts:
        self.thoughts[mood].append(thought)
     else:
        self.thoughts[mood] = [thought]

    def add_rule(self, category, rule):
     if category in self.rules:
        self.rules[category].append(rule)
     else:
        self.rules[category] = [rule]

    def generate_thought(self, mood):
        if mood == "Very sad":
            mood = "sad"
        elif mood == "Very happy":
            mood = "happy"
        elif mood == "Happy":
            mood = "happy"
        elif mood == "Sad":
            mood = "sad"
        if mood not in self.thoughts:
            mood = "happy"
        thought = random.choice(self.thoughts[mood])
        if thought == self.thoughts[mood][0]:
         return thought + ". " + random.choice(self.rules["weather"])
        elif thought == self.thoughts[mood][1]:
         return thought + ". " + random.choice(self.rules["friend"])
        elif thought == self.thoughts[mood][2]:
         return thought + ". " + random.choice(self.rules["dinner"])
        elif thought == self.thoughts[mood][3]:
         return thought + ". " + random.choice(self.rules["project"])
        else:
         return thought + ". " + random.choice(self.rules["vacation"])

    def do_tick(self):
        self.thought = self.generate_thought(self.mood_as_string())
        print(self.thought)

    def run_every_3_minutes(self):
     global stop
     if not stop:
        self.do_tick()
        self.timer = threading.Timer(180, self.run_every_3_minutes) #180
        self.timer.daemon = True
        self.timer.start()

    def start(self):
        # Start the repeating function in a separate thread
        thread = threading.Thread(target=self.run_every_3_minutes)
        thread.start()

if __name__ == '__main__':
    b = Brain()
    b.start()
    b.update_mood("I hate you so much")
    b.update_mood("I love you so much")
    print(b.mood_as_string())

# Example usage of the Brain class
# b = Brain()
# b.update_mood("I hate you so much")
# b.update_mood("I love you so much")
# print(b.mood_as_string())
# b.plot_mood_history()
