import pandas as pd
import jenkins
import pickle

# Load the model and important features
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    important_features = pd.read_csv('important_features.csv')
except FileNotFoundError as e:
    print(f"Error loading model or important features: {str(e)}")
    model = None
    important_features = pd.DataFrame()

# Connect to Jenkins
server = jenkins.Jenkins('http://localhost:8080/', username='mahesh4434', password='Dada@7744')
job_name = 'GCP_Apply'

def get_recommendations(build_number):
    # Example function to get recommendations based on build number
    # Use your trained model to generate recommendations
    # This is a placeholder function
    return 'Optimize resource allocation for step X.'

# Get the last build number
build_info = server.get_build_info(job_name, 'lastBuild')
build_number = build_info['number']
recommendations = get_recommendations(build_number)

# Display recommendations in the Jenkins console or custom dashboard
print(f'Recommendations for build {build_number}: {recommendations}')
