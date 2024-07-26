import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load your dataset
data = pd.read_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\pipeline_data.csv')  # Updated path

# Preprocessing steps
X = data.drop('build_success', axis=1)
y = data['build_success']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the preprocessed data
pd.DataFrame(X_train).to_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\X_train.csv', index=False)  # Updated path
pd.DataFrame(X_test).to_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\X_test.csv', index=False)  # Updated path
pd.DataFrame(y_train).to_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\y_train.csv', index=False)  # Updated path
pd.DataFrame(y_test).to_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\y_test.csv', index=False)  # Updated path
