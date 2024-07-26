import sys
import joblib
import numpy as np

def predict_pipeline_success(num_commits, num_tests, test_pass_rate, previous_build_result, lines_of_code_changed):
    # Load the trained model
    model = joblib.load('pipeline_predictor.pkl')
    
    # Prepare the input features
    features = np.array([[num_commits, num_tests, test_pass_rate, previous_build_result, lines_of_code_changed]])
    
    # Make prediction
    prediction = model.predict(features)
    
    # Output result
    if prediction[0] == 1:
        return 'success'
    else:
        return 'fail'

if __name__ == "__main__":
    num_commits = int(sys.argv[1])
    num_tests = int(sys.argv[2])
    test_pass_rate = float(sys.argv[3])
    previous_build_result = int(sys.argv[4])
    lines_of_code_changed = int(sys.argv[5])
    
    result = predict_pipeline_success(num_commits, num_tests, test_pass_rate, previous_build_result, lines_of_code_changed)
    print(result)
