import datetime
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

# Sample historical data
historical_data = [
    {"time_of_day": "morning", "art_style": "minimalistic", "window_style": "dark", "rating": 4},
    {"time_of_day": "afternoon", "art_style": "abstract", "window_style": "mica", "rating": 5},
    {"time_of_day": "evening", "art_style": "classic", "window_style": "win7", "rating": 3},
    {"time_of_day": "night", "art_style": "bright", "window_style": "light", "rating": 5},
    {"time_of_day": "night", "art_style": "bright", "window_style": "aero", "rating": 5},
    # Add more historical data...
]

def choose_window_style(time_of_day, favorite_art_style):
    # Prepare the training data
    X_train = []
    y_train = []
    for data in historical_data:
        X_train.append([data["time_of_day"], data["art_style"]])
        y_train.append(data["window_style"])

    # Encode categorical variables using one-hot encoding
    encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
    X_train_encoded = encoder.fit_transform(X_train)

    # Train a machine learning model
    model = RandomForestClassifier()
    model.fit(X_train_encoded, y_train)

    # Make predictions
    X_test = [[time_of_day, favorite_art_style]]
    X_test_encoded = encoder.transform(X_test)
    predicted_styles = model.predict(X_test_encoded)

    # Retrieve ratings for predicted styles
    style_ratings = []
    for data in historical_data:
        if data["window_style"] == predicted_styles[0]:
            style_ratings.append(data["rating"])

    # Calculate the average rating for the predicted styles
    average_rating = sum(style_ratings) / len(style_ratings) if style_ratings else 0

    # Retrieve all styles with the highest rating
    top_styles = [data["window_style"] for data in historical_data if data["rating"] == max(style_ratings)]

    # Randomly select a style from the top-rated styles
    selected_style = random.choice(top_styles) if top_styles else "default"

    # Store the user feedback in historical data
    print(top_styles)
    print(selected_style)
    user_rating = int(input("Please rate the suggested window style (1-5): "))
    historical_data.append({"time_of_day": time_of_day, "art_style": favorite_art_style, "window_style": selected_style, "rating": user_rating})

    return selected_style

# Example usage
while True:
 time_of_day = "evening"  # You can replace this with the actual time of day
 favorite_art_style = "abstract"  # You can replace this with the user's favorite art style

 window_style = choose_window_style(time_of_day, favorite_art_style)
 print("Selected window style:", window_style)
