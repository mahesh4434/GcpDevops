import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the data
data = pd.read_json('jenkins_build_data.json')

# Preprocess the data
data['duration'] = data['duration'] / 1000  # Convert duration to seconds
data = pd.get_dummies(data, columns=['result'], drop_first=True)

# Split the data
X = data.drop(['result'], axis=1)
y = data['result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Save the model and important features
import pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

feature_importances = model.feature_importances_
feature_names = X_train.columns
important_features = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
important_features.sort_values(by='Importance', ascending=False, inplace=True)
important_features.to_csv('important_features.csv', index=False)
