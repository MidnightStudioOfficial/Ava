import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import random
import threading
import tkinter as tk

stop = False

class Traits:
    def __init__(self):
        self.traits_available = {
            "depression": {
                "mood_score": -0.5
            }
        }

class Brain:
    def __init__(self):
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
        self.vectorizer = CountVectorizer()

        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def update_mood(self, text):
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        sentiment_score = sentiment_scores["compound"]
        self.mood += sentiment_score
        self.mood_history.append(self.mood)

    def get_mood(self):
        return self.mood

    def reset_mood(self):
        self.mood = 0.0
        self.mood_history = []

    def mood_as_string(self):
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
        return self.mood_history

    def plot_mood_history(self):
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

    def update_memory(self, thought):
        if thought not in self.memory:
            self.memory[thought] = 1
        else:
            self.memory[thought] += 1

    def generate_personalized_thought(self, mood):
        mood_category = mood.lower()
        if mood_category not in self.memory:
            mood_category = "happy"
        thoughts = list(self.memory.keys())
        X = self.vectorizer.fit_transform(thoughts)
        vectorizer = CountVectorizer()
        vectorizer.fit_transform(thoughts + [self.thought])
        thought_vector = vectorizer.transform([self.thought])
        cosine_similarities = cosine_similarity(X, thought_vector).flatten()
        related_thought_indices = cosine_similarities.argsort()[:-2:-1]
        related_thought = thoughts[related_thought_indices[0]]
        return related_thought

    def do_tick(self):
        self.thought = self.generate_thought(self.mood_as_string())
        self.update_memory(self.thought)
        personalized_thought = self.generate_personalized_thought(self.mood_as_string())
        print(f"Generated Thought: {self.thought}")
        print(f"Personalized Thought: {personalized_thought}")

    def run_every_3_minutes(self):
        global stop
        if not stop:
            self.do_tick()
            self.timer = threading.Timer(180, self.run_every_3_minutes)
            self.timer.daemon = True
            self.timer.start()

    def start(self):
        thread = threading.Thread(target=self.run_every_3_minutes)
        thread.start()


def interact_with_brain(brain):
    def update_mood():
        user_text = user_entry.get()
        brain.update_mood(user_text)
        mood_label["text"] = brain.mood_as_string()
        # print("UPDATE")

    def generate_thought():
        thought = brain.generate_thought(brain.mood_as_string())
        thought_text["text"] = thought

    def show_mood_history():
        mood_history = brain.get_mood_history()
        plt.plot(mood_history)
        plt.title("Mood History")
        plt.xlabel("Time")
        plt.ylabel("Mood")
        plt.show()

    root = tk.Tk()
    root.title("Simulated Brain")

    mood_label = tk.Label(root, text="Neutral")
    mood_label.pack()

    user_entry = tk.Entry(root)
    user_entry.pack()

    update_mood_button = tk.Button(root, text="Update Mood", command=update_mood)
    update_mood_button.pack()

    thought_text = tk.Label(root, text="")
    thought_text.pack()

    generate_thought_button = tk.Button(root, text="Generate Thought", command=generate_thought)
    generate_thought_button.pack()

    mood_history_button = tk.Button(root, text="View Mood History", command=show_mood_history)
    mood_history_button.pack()

    root.mainloop()


class AdaptiveBrain(Brain):
    def __init__(self):
        super().__init__()
        self.feedback_vectorizer = TfidfVectorizer()
        self.feedback_classifier = MultinomialNB()

    def update_memory(self, thought):
        super().update_memory(thought)
        self.update_feedback_classifier()

    def update_feedback_classifier(self):
        thoughts = list(self.memory.keys())
        feedback = [1 if thought in self.thoughts[self.mood_as_string()] else 0 for thought in thoughts]
        X = self.feedback_vectorizer.fit_transform(thoughts)
        self.feedback_classifier.fit(X, feedback)

    def generate_personalized_thought(self, mood):
        mood_category = mood.lower()
        if mood_category not in self.memory:
            mood_category = "happy"
        thoughts = list(self.memory.keys())
        X = self.feedback_vectorizer.transform(thoughts)
        related_thought = None

        if X.shape[0] > 0:
            predicted_feedback = self.feedback_classifier.predict(X)
            best_match_index = predicted_feedback.argmax()
            related_thought = thoughts[best_match_index]

        if related_thought is None:
            related_thought = super().generate_personalized_thought(mood)

        return related_thought



if __name__ == '__main__':
    b = Brain()
    b.start()
    interact_with_brain(b)