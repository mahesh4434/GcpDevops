import jenkins
import pickle
import pandas as pd
from flask import Flask, render_template_string

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

def get_pipeline_data(job_name, build_number):
    build_info = server.get_build_info(job_name, build_number)
    stages = build_info['actions'][0].get('stages', [])
    pipeline_data = []
    for stage in stages:
        stage_data = {
            'name': stage['name'],
            'status': stage['status'],
            'durationMillis': stage['durationMillis']
        }
        pipeline_data.append(stage_data)
    return pipeline_data

# Get the last build number
build_info = server.get_build_info(job_name, 'lastBuild')
build_number = build_info['number']
recommendations = get_recommendations(build_number)

# Get pipeline data for the last build
pipeline_data = get_pipeline_data(job_name, build_number)

# Create a Flask application
app = Flask(__name__)

@app.route('/')
def index():
    # Create HTML content
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jenkins Build Recommendations</title>
    </head>
    <body>
        <h1>Recommendations for Build {{ build_number }}</h1>
        <p>{{ recommendations }}</p>
        <h2>Pipeline Stages</h2>
        <table border="1">
            <tr>
                <th>Stage Name</th>
                <th>Status</th>
                <th>Duration (ms)</th>
            </tr>
    '''
    for stage in pipeline_data:
        html_content += f'''
            <tr>
                <td>{stage['name']}</td>
                <td>{stage['status']}</td>
                <td>{stage['durationMillis']}</td>
            </tr>
        '''
    html_content += '''
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_content, build_number=build_number, recommendations=recommendations)

if __name__ == '__main__':
    app.run(port=5000)
