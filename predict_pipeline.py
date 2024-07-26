import joblib
import sys
import numpy as np

# Load the model
model = joblib.load('pipeline_predictor.pkl')

# Example features for the new pipeline run
num_commits = int(sys.argv[1])
num_tests = int(sys.argv[2])
test_pass_rate = float(sys.argv[3])
previous_build_result = int(sys.argv[4])
lines_of_code_changed = int(sys.argv[5])

# Prepare feature array
features = np.array([[num_commits, num_tests, test_pass_rate, previous_build_result, lines_of_code_changed]])

# Predict
prediction = model.predict(features)
if prediction[0] == 1:
    print("The pipeline is predicted to succeed.")
else:
    print("The pipeline is predicted to fail.")
