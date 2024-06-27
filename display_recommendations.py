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

def get_build_data(job_name):
    job_info = server.get_job_info(job_name)
    builds = job_info['builds']

    data = []
    for build in builds:
        build_info = server.get_build_info(job_name, build['number'])
        data.append({
            'number': build['number'],
            'result': build_info['result'],
            'duration': build_info['duration'],
            'timestamp': build_info['timestamp']
        })
    return data

def get_pipeline_data(job_name, build_number):
    build_info = server.get_build_info(job_name, build_number)
    stages = build_info['actions'][0]['stages']
    pipeline_data = []
    for stage in stages:
        pipeline_data.append({
            'name': stage['name'],
            'status': stage['status'],
            'duration': stage['durationMillis'],
            'start_time': stage['startTimeMillis']
        })
    return pipeline_data

# Get the last build number
build_info = server.get_build_info(job_name, 'lastBuild')
build_number = build_info['number']
recommendations = get_recommendations(build_number)
build_data = get_build_data(job_name)
pipeline_data = get_pipeline_data(job_name, build_number)

# Flask application
app = Flask(__name__)

@app.route('/')
def home():
    # Generate HTML content
    html_content = f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Jenkins Build Recommendations</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid black;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>Recommendations for Build {build_number}</h1>
          <p>{recommendations}</p>
          <h2>Build Data</h2>
          <table>
            <tr>
              <th>Build Number</th>
              <th>Result</th>
              <th>Duration (seconds)</th>
              <th>Timestamp</th>
            </tr>
    '''
    for build in build_data:
        html_content += f'''
        <tr>
          <td>{build['number']}</td>
          <td>{build['result']}</td>
          <td>{build['duration'] / 1000}</td>
          <td>{build['timestamp']}</td>
        </tr>
        '''
    
    html_content += '''
          </table>
          <h2>Pipeline Stages Data for Build {build_number}</h2>
          <table>
            <tr>
              <th>Stage Name</th>
              <th>Status</th>
              <th>Duration (milliseconds)</th>
              <th>Start Time (milliseconds)</th>
            </tr>
    '''
    for stage in pipeline_data:
        html_content += f'''
        <tr>
          <td>{stage['name']}</td>
          <td>{stage['status']}</td>
          <td>{stage['duration']}</td>
          <td>{stage['start_time']}</td>
        </tr>
        '''
    
    html_content += '''
          </table>
        </div>
      </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)

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
