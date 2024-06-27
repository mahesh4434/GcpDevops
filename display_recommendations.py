import jenkins
import pandas as pd
import pickle
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import re

# Jenkins details
jenkins_url = 'http://localhost:8080/'
username = 'mahesh4434'
api_token = '11b9d314ad7cd85e9661733d0ddba3c9c8'  # Provided API token
job_name = 'GCP_Apply'

# Load the model
model_path = r'D:\New folder\POC\model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Function to get CSRF crumb
def get_crumb(jenkins_url, username, api_token):
    crumb_url = jenkins_url + 'crumbIssuer/api/json'
    response = requests.get(crumb_url, auth=HTTPBasicAuth(username, api_token))
    response.raise_for_status()
    return response.json()

# Get CSRF crumb
crumb = get_crumb(jenkins_url, username, api_token)
crumb_header = crumb['crumbRequestField']
crumb_value = crumb['crumb']

# Initialize Jenkins server
server = jenkins.Jenkins(jenkins_url, username=username, password=api_token)

# Fetch latest build info
try:
    latest_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
    latest_build_info = server.get_build_info(job_name, latest_build_number)
except Exception as e:
    print(f"Error fetching build info: {e}")
    raise

# Generate recommendations based on the model
build_data = {
    'number': latest_build_info['number'],
    'result': latest_build_info['result'],
    'duration': latest_build_info['duration'],
    'timestamp': datetime.fromtimestamp(latest_build_info['timestamp'] / 1000.0)
}

build_df = pd.DataFrame([build_data])
build_df['duration'] = build_df['duration'] / 1000
build_df = pd.get_dummies(build_df, columns=['result'], drop_first=True)
if 'timestamp' in build_df.columns:
    build_df['timestamp'] = pd.to_numeric(build_df['timestamp'])

# Ensure `number` column is present in X_latest for prediction
X_latest = build_df[['number', 'duration', 'timestamp']]  # Include 'number' feature here

# Predict recommendations
try:
    recommendations = model.predict(X_latest)
    print("Recommendations:", recommendations)
except Exception as e:
    print(f"Error predicting recommendations: {e}")
    raise

# Update Jenkins job description
try:
    job_config = server.get_job_config(job_name)
    new_description = f"<description>Recommendations: {recommendations[0]}</description>"
    updated_config = re.sub(r'<description>.*?</description>', new_description, job_config, flags=re.DOTALL)
    
    headers = {
        crumb_header: crumb_value,
        'Content-Type': 'application/xml'
    }
    config_url = f"{jenkins_url}job/{job_name}/config.xml"
    response = requests.post(config_url, data=updated_config, auth=HTTPBasicAuth(username, api_token), headers=headers)
    response.raise_for_status()
    print("Job description updated successfully")
except Exception as e:
    print(f"Error updating job description: {e}")
    raise

