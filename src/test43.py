import datetime
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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
    encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
    X = encoder.fit_transform([[d["time_of_day"], d["art_style"]] for d in historical_data])
    y = [d["window_style"] for d in historical_data]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a machine learning model (Random Forest Classifier) and perform hyperparameter tuning if needed
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Make predictions
    X_test_encoded = encoder.transform([[time_of_day, favorite_art_style]])
    predicted_style = model.predict(X_test_encoded)[0]

    # Store the user feedback in historical data
    print(predicted_style)
    user_rating = int(input("Please rate the suggested window style (1-5): "))
    historical_data.append({"time_of_day": time_of_day, "art_style": favorite_art_style, "window_style": predicted_style, "rating": user_rating})

    return predicted_style

# Example usage
while True:
    time_of_day = "evening"  # You can replace this with the actual time of day
    favorite_art_style = "abstract"  # You can replace this with the user's favorite art style

    window_style = choose_window_style(time_of_day, favorite_art_style)
    print("Selected window style:", window_style)
