import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    # Load the preprocessed data
    data = pd.read_csv('processed_pipeline_data.csv')
    
    # Features and target variable
    X = data.drop('build_success', axis=1)
    y = data['build_success']
    
    # Initialize and train the model
    model = RandomForestClassifier()
    model.fit(X, y)
    
    # Save the trained model
    joblib.dump(model, 'pipeline_predictor.pkl')

if __name__ == "__main__":
    train_model()
