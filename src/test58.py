import torch
import torch.nn as nn

class MoodPredictor(nn.Module):
    def __init__(self):
        super(MoodPredictor, self).__init__()
        self.fc1 = nn.Linear(7, 10)  # Adjusted input size to match the concatenated tensor
        self.fc2 = nn.Linear(10, 10)
        self.fc3 = nn.Linear(10, 1)
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = self.fc3(x)
        return x

# Create an instance of the MoodPredictor class
model = MoodPredictor()

# Define the input data
time_of_day = torch.tensor([1, 0, 1])  # Example time of day input
personality_traits = torch.tensor([0.2, 0.4, 0.6])  # Example personality traits input
sentiment_score = torch.tensor([-0.9])  # Example text sentiment score input

# Adjusted input sizes to match the dimensions
time_of_day = time_of_day.unsqueeze(0)
personality_traits = personality_traits.unsqueeze(0)
sentiment_score = sentiment_score.unsqueeze(0)

# Concatenate the input data
input_data = torch.cat((time_of_day, personality_traits, sentiment_score), dim=1)  # Concatenate along the second dimension

# Perform the forward pass to get the mood prediction
mood_prediction = model(input_data)

print("Mood prediction:", mood_prediction.item())
