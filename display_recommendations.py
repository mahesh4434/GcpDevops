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
    # Placeholder recommendation logic
    return 'Optimize resource allocation for step X.'

# Get the last build number
build_info = server.get_build_info(job_name, 'lastBuild')
build_number = build_info['number']
recommendations = get_recommendations(build_number)

# Update job description with recommendations
job_description = server.get_job_config(job_name)
new_description = f"{job_description}\nRecommendations: {recommendations}"
server.reconfig_job(job_name, new_description)

# Create a Flask app to serve the recommendations
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <html>
        <head>
            <title>Jenkins Build Recommendations</title>
        </head>
        <body>
            <h1>Recommendations for Jenkins Build {{ build_number }}</h1>
            <p>{{ recommendations }}</p>
        </body>
    </html>
    """, build_number=build_number, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
