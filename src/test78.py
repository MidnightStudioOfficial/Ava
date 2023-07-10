import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Exercise data
exercises = [
    {
        "name": "Deep Breathing",
        "description": "Take slow, deep breaths in and out.",
        "duration": 5  # in minutes
    },
    {
        "name": "Body Scan",
        "description": "Scan your body for any tension or discomfort.",
        "duration": 10
    },
    # Add more exercises here
]

# User data (example)
user_data = [
    {
        "exercise": "Deep Breathing",
        "rating": 5,
        "comment": "I really enjoyed this exercise."
    },
    {
        "exercise": "Body Scan",
        "rating": 4,
        "comment": "It helped me relax and release tension."
    },
    # Add more user data here
]

# Convert user data to a DataFrame
user_df = pd.DataFrame(user_data)

class MeditationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meditation App")

        self.timer_label = tk.Label(root, text="")
        self.timer_label.pack()

        self.exercise_label = tk.Label(root, text="Choose an Exercise:")
        self.exercise_label.pack()

        self.exercise_options = [exercise["name"] for exercise in exercises]

        self.selected_exercise = tk.StringVar(root)
        self.selected_exercise.set(self.exercise_options[0])  # Set the default exercise

        self.exercise_dropdown = tk.OptionMenu(root, self.selected_exercise, *self.exercise_options)
        self.exercise_dropdown.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_exercise)
        self.start_button.pack()

    def start_exercise(self):
        selected_exercise = self.selected_exercise.get()
        exercise = [ex for ex in exercises if ex["name"] == selected_exercise][0]
        self.exercise_name = exercise["name"]
        self.exercise_description = exercise["description"]
        duration_minutes = exercise["duration"]
        duration_seconds = duration_minutes * 60

        # Display a message box with exercise details
        messagebox.showinfo("Exercise", f"Exercise: {self.exercise_name}\nDuration: {duration_minutes} minutes")

        self.update_timer(duration_seconds)  # Start the timer

    def update_timer(self, remaining_time):
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"Time Remaining: {minutes:02d}:{seconds:02d}"
        self.timer_label.configure(text=timer_text)

        if remaining_time > 0:
            self.root.after(1000, self.update_timer, remaining_time - 1)
        else:
            self.show_next_exercise()

    def show_next_exercise(self):
        # Display a message box to indicate the end of the exercise
        messagebox.showinfo("Exercise", "Exercise completed!")

        # Get personalized recommendations
        recommendations = self.get_personalized_recommendations()

        # Display the recommendations to the user
        messagebox.showinfo("Recommendations", f"Personalized Recommendations:\n{recommendations}")

        # Start the next exercise
        self.start_exercise()

    def get_personalized_recommendations(self):
        # Convert exercise data to a DataFrame
        exercise_df = pd.DataFrame(exercises)

        # Merge exercise and user data on exercise name
        merged_df = pd.merge(user_df, exercise_df, left_on='exercise', right_on='name')

        # Prepare data for recommendation using TF-IDF vectorization
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(merged_df['description'])

        # Compute cosine similarity between exercises
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        # Get the index of the last completed exercise
        last_completed_index = merged_df.index[-1]

        # Get the cosine similarity scores for the last completed exercise
        similarity_scores = list(enumerate(cosine_sim[last_completed_index]))

        # Sort the exercises based on similarity scores
        sorted_exercises = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Get the top 3 recommended exercises (excluding the last completed exercise)
        recommended_exercises = []
        for exercise_index, score in sorted_exercises[1:4]:
            recommended_exercises.append(exercise_df['name'][exercise_index])

        return recommended_exercises


root = tk.Tk()
app = MeditationApp(root)
root.mainloop()
