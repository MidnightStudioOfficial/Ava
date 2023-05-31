import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

class Brain:
    def __init__(self):
        # Initialize mood to 0.0 and create an empty list for mood history
        self.mood = 0.0
        self.mood_history = []
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

# Example usage of the Brain class
# b = Brain()
# b.update_mood("I hate you so much")
# b.update_mood("I love you so much")
# print(b.mood_as_string())
# b.plot_mood_history()
