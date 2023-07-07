import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Generate some dummy data for training
num_samples = 2
time_of_day = [1, 0]  # Random time values between 0 and 1
personality_traits = np.random.rand(num_samples, 5)  # Random personality traits as a 2D array
sentiment_score = [-0.4, -0.3]  # Random sentiment scores between 0 and 1
mood = [-0.9, -0.7]  # Random mood values between 0 and 1

# Create the neural network model
model = Sequential()
model.add(Dense(10, input_dim=7, activation='relu'))  # Adjust input_dim based on the number of features
model.add(Dense(1, activation='linear'))  # Output a single float mood value

# Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# Train the model
model.fit(np.hstack((time_of_day.reshape(-1, 1), personality_traits, sentiment_score.reshape(-1, 1))), mood, epochs=10, batch_size=32)  # Adjust epochs and batch_size as needed

# Now you can use the trained model to make predictions
time_of_day_test = np.array([0.8])  # Example test values
personality_traits_test = np.array([[0.2, 0.3, 0.4, 0.5, 0.6]])
sentiment_score_test = np.array([0.7])
mood_prediction = model.predict(np.hstack((time_of_day_test.reshape(-1, 1), personality_traits_test, sentiment_score_test.reshape(-1, 1))))
print("Predicted mood:", mood_prediction[0][0])
