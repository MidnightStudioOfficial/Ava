from nltk.sentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self) -> None:
        """
        Initializes the SentimentAnalyzer object.

        Sets the mood to 0.0 and creates an empty list for mood history.
        Creates an instance of the SentimentIntensityAnalyzer class.
        """
        # Initialize mood to 0.0 and create an empty list for mood history
        self.mood: float = 0.0

        # Create an instance of the SentimentIntensityAnalyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def update_mood(self, text: str) -> None:
        """
        Updates the mood of the SentimentAnalyzer object by adding the sentiment score of the given text.

        Args:
            text (str): The text to be analyzed.

        Returns:
            None.
        """
        # Get the sentiment scores for the given text
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        # Get the compound score from the sentiment scores
        sentiment_score = sentiment_scores["compound"]
        # Update the mood by adding the sentiment score
        self.mood += sentiment_score

    def get_mood(self) -> float:
        """
        Returns the current mood of the SentimentAnalyzer object.

        Returns:
            float: The current mood of the SentimentAnalyzer object.
        """
        # Return the current mood
        return self.mood

    def reset_mood(self):
        """
        Resets the mood of the SentimentAnalyzer object to 0.0.

        Returns:
            None.
        """
        # Reset the mood to 0.0 and clear the mood history list
        self.mood = 0.0

    def mood_as_emoji(self):
        """
        Returns the mood of the SentimentAnalyzer object as an emoji.

        Returns:
            str: The mood of the SentimentAnalyzer object as an emoji.
        """
        if self.mood > 1.0:
            return "😄😄"
        elif self.mood > 0.75:
            return "😄"
        elif self.mood > 0.5:
            return "🙂"
        elif self.mood > 0:
            return "😊"
        elif self.mood == 0:
            return "😐"
        elif self.mood > -0.5:
            return "😞"
        elif self.mood > -0.75:
            return "😢"
        else:
            return "😢😢"
