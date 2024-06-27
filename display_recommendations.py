import jenkins
import pickle
import pandas as pd

# Load the model and important features
with open(r'D:\New folder\POC\model.pkl', 'rb') as f:
    model = pickle.load(f)

important_features = pd.read_csv(r'D:\New folder\POC\important_features.csv')

# Connect to Jenkins
server = jenkins.Jenkins('http://localhost:8080/', username='mahesh4434', password='Dada@7744')
job_name = 'GCP_Apply'

def get_recommendations(build_number):
    # Example function to get recommendations based on build number
    # Use your trained model to generate recommendations
    # This is a placeholder function
    # Replace this with your actual logic to generate recommendations
    # For example, use the model to predict based on important features
    # Here, we are assuming a placeholder recommendation.
    return 'Optimize resource allocation for step X.'

# Get the last build number
build_info = server.get_build_info(job_name, 'lastBuild')
build_number = build_info['number']
recommendations = get_recommendations(build_number)

# Display recommendations in the Jenkins console or custom dashboard
print(f'Recommendations for build {build_number}: {recommendations}')

# Example: Push recommendations to a CI/CD dashboard (pseudo-code)
# Replace this with actual implementation to integrate with your dashboard
# For example, use Jenkins API to update a dashboard or use a Jenkins plugin

# Sample pseudo-code to update a Jenkins job description with recommendations
job_description = server.get_job_config(job_name)
new_description = f"{job_description}\nRecommendations: {recommendations}"
server.reconfig_job(job_name, new_description)

# Example: Update a custom dashboard with recommendations (pseudo-code)
# Replace this with actual implementation to update your custom dashboard
# For example, if you have a custom web dashboard, use APIs to push data

# Assuming you have a custom dashboard API endpoint
dashboard_url = 'http://your-custom-dashboard-api/recommendations'
payload = {'build_number': build_number, 'recommendations': recommendations}
response = requests.post(dashboard_url, json=payload)

if response.status_code == 200:
    print(f'Recommendations pushed to dashboard successfully.')
else:
    print(f'Failed to push recommendations to dashboard. Status Code: {response.status_code}')
