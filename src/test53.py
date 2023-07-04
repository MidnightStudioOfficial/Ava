import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Step 1: Load the Data
data = pd.read_csv('labeled_dataset.csv')  # Replace 'labeled_dataset.csv' with your actual file name

# Step 2: Split the data into features (X) and target (y)
X = data['text']
y = data['topic']

# Step 3: Preprocess the Data and Prepare the Target Labels
# Using a pipeline to combine vectorizer and classifier
# This will help avoid data leakage during cross-validation
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(lowercase=True)),
    ('classifier', SVC())
])

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Hyperparameter tuning using GridSearchCV
# Define the hyperparameters to search
param_grid = {
    'vectorizer__ngram_range': [(1, 1), (1, 2)],  # Try different n-gram ranges
    'classifier__C': [1, 10],  # Try different values of the regularization parameter C
    'classifier__kernel': ['linear', 'rbf']  # Try different kernel functions
}

# Create the GridSearchCV object
grid_search = GridSearchCV(pipeline, param_grid, cv=3)  # Changed from cv=5 to cv=3

# Fit the grid search to find the best model
grid_search.fit(X_train, y_train)

# Step 6: Predict the Topics
new_text = ['ml and ai is the best']

predicted_topic = grid_search.predict(new_text)
print(predicted_topic)
