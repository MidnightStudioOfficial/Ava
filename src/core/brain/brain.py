import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

class Brain:
    def __init__(self):
        self.mood = 0.0
        self.mood_history = []
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

# b = Brain()
# b.update_mood("I hate you so much")
# b.update_mood("I love you so much")
# print(b.mood_as_string())
# b.plot_mood_history()
