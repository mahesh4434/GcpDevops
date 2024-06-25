import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json
import pickle  # Import pickle module directly

# Load the data from JSON file
try:
    with open('jenkins_build_data.json', 'r') as f:
        data = json.load(f)
    data = pd.DataFrame(data)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading data: {str(e)}")
    data = pd.DataFrame()

# Check if data is loaded successfully and contains necessary columns
if not data.empty and 'result' in data.columns:
    # Preprocess the data
    data['duration'] = data['duration'] / 1000  # Convert duration to seconds
    data = pd.get_dummies(data, columns=['result'], drop_first=True)

    # Check again after preprocessing
    if 'result' in data.columns:
        # Split the data
        X = data.drop(['result'], axis=1)
        y = data['result']  # Assuming 'result' is your target variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

        # Save the model as model.pkl
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)

        # Save important features as important_features.csv
        feature_importances = model.feature_importances_
        feature_names = X_train.columns
        important_features = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
        important_features.sort_values(by='Importance', ascending=False, inplace=True)
        important_features.to_csv('important_features.csv', index=False)
    else:
        print("After preprocessing, 'result' column not found. Check data preprocessing steps.")
else:
    print("No data loaded or 'result' column not found. Check your data file or loading process.")
