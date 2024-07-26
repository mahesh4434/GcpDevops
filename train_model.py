import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load preprocessed data
X_train = pd.read_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\X_train.csv')  # Updated path
X_test = pd.read_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\X_test.csv')  # Updated path
y_train = pd.read_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\y_train.csv').values.ravel()  # Updated path
y_test = pd.read_csv('D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\y_test.csv').values.ravel()  # Updated path

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# Save the model
joblib.dump(model, 'pipeline_predictor.pkl')
