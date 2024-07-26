import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# Use path from Jenkins workspace
data_path = os.path.join(os.getcwd(), 'pipeline_data.csv')

# Create a dummy data file if not present (for demonstration)
if not os.path.exists(data_path):
    dummy_data = pd.DataFrame({
        'num_commits': [5, 3, 10],
        'num_tests': [100, 80, 120],
        'test_pass_rate': [0.95, 0.85, 0.90],
        'previous_build_result': [1, 0, 1],
        'lines_of_code_changed': [50, 20, 80],
        'build_success': [1, 0, 1]
    })
    dummy_data.to_csv(data_path, index=False)

data = pd.read_csv(data_path)

# Preprocessing steps
X = data.drop('build_success', axis=1)
y = data['build_success']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_t
