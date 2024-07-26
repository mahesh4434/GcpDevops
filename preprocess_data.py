import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os


# Use path from Jenkins workspace
data_path = os.path.join(os.getcwd(), 'pipeline_data.csv')

if not os.path.isfile(data_path):
    raise FileNotFoundError(f"Data file not found: {data_path}")

data = pd.read_csv(data_path)

# Preprocessing steps
X = data.drop('build_success', axis=1)
y = data['build_success']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the preprocessed data in Jenkins workspace
X_train_path = os.path.join(os.getcwd(), 'X_train.csv')
X_test_path = os.path.join(os.getcwd(), 'X_test.csv')
y_train_path = os.path.join(os.getcwd(), 'y_train.csv')
y_test_path = os.path.join(os.getcwd(), 'y_test.csv')

pd.DataFrame(X_train).to_csv(X_train_path, index=False)
pd.DataFrame(X_test).to_csv(X_test_path, index=False)
pd.DataFrame(y_train).to_csv(y_train_path, index=False)
pd.DataFrame(y_test).to_csv(y_test_path, index=False)
