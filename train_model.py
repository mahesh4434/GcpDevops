# Import necessary libraries
import pandas as pd

# Load your data
data = pd.read_csv('path_to_your_data.csv')  # Replace with your actual data path

# Check if 'result' column exists before dropping it
if 'result' in data.columns:
    X = data.drop(['result'], axis=1)
else:
    print("'result' column not found in the dataset.")

# Continue with your model training and other steps
# Example:
# model.fit(X, y)
# predictions = model.predict(X)
