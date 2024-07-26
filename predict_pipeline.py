import pickle
import sys

def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def predict_success(model, features):
    # Assuming features are passed as a space-separated string
    features = [float(x) for x in features.split()]
    prediction = model.predict([features])
    return prediction[0]

if __name__ == "__main__":
    model_path = 'D:\\New folder\\DevOpsPOC\\DevOpsGeniAiPart\\CSV files\\pipeline_predictor.pkl'
    features = sys.argv[1]  # Features should be passed as a command line argument
    
    model = load_model(model_path)
    result = predict_success(model, features)
    
    if result == 1:
        print("The pipeline is expected to succeed.")
        sys.exit(0)
    else:
        print("The pipeline is expected to fail.")
        sys.exit(1)
