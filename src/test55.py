import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Define the neural network model
class MoodNet(nn.Module):
    def __init__(self):
        super(MoodNet, self).__init__()
        self.fc1 = nn.Linear(7, 10)  # Adjust input size based on the number of features
        self.fc2 = nn.Linear(10, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Generate some dummy data for training
num_samples = 10
time_of_day = np.random.rand(num_samples, 1)  # Random time values between 0 and 1
personality_traits = np.random.rand(num_samples, 5)  # Random personality traits as a 2D array
sentiment_score = np.random.rand(num_samples, 1)  # Random sentiment scores between 0 and 1
mood = np.random.rand(num_samples, 1)  # Random mood values between 0 and 1

# Convert data to PyTorch tensors
time_of_day = torch.from_numpy(time_of_day).float()
personality_traits = torch.from_numpy(personality_traits).float()
sentiment_score = torch.from_numpy(sentiment_score).float()
mood = torch.from_numpy(mood).float()

# Concatenate the input tensors
inputs = torch.cat((time_of_day, personality_traits, sentiment_score), dim=1)

# Create the neural network model
model = MoodNet()

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters())

# Train the model
num_epochs = 10
batch_size = 32

for epoch in range(num_epochs):
    for i in range(0, num_samples, batch_size):
        batch_inputs = inputs[i:i+batch_size]
        batch_mood = mood[i:i+batch_size]

        # Forward pass
        outputs = model(batch_inputs)
        loss = criterion(outputs, batch_mood)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Now you can use the trained model to make predictions
time_of_day_test = np.array([[0.8]])  # Example test values
personality_traits_test = np.array([[0.2, 0.3, 0.4, 0.5, 0.6]])
sentiment_score_test = np.array([[0.7]])

# Convert test data to PyTorch tensors
time_of_day_test = torch.from_numpy(time_of_day_test).float()
personality_traits_test = torch.from_numpy(personality_traits_test).float()
sentiment_score_test = torch.from_numpy(sentiment_score_test).float()

# Concatenate the test tensors
test_inputs = torch.cat((time_of_day_test, personality_traits_test, sentiment_score_test), dim=1)

# Make predictions
model.eval()
with torch.no_grad():
    mood_prediction = model(test_inputs)
    print("Predicted mood:", mood_prediction.item())
