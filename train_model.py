import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Use path from Jenkins workspace
X_train_path = os.path.join(os.getcwd(), 'X_train.csv')
X_test_path = os.path.join(os.getcwd(), 'X_test.csv')
y_train_path = os.path.join(os.getcwd(), 'y_train.csv')
y_test_path = os.path.join(os.getcwd(), 'y_test.csv')

X_train = pd.read_csv(X_train_path)
X_test = pd.read_csv(X_test_path)
y_train = pd.read_csv(y_train_path).values.ravel()
y_test = pd.read_csv(y_test_path).values.ravel()

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy}')

# Save the model in Jenkins workspace
model_path = os.path.join(os.getcwd(), 'pipeline_predictor.pkl')
joblib.dump(model, model_path)
