import json
import pickle
import pandas as pd
from flask import Flask, render_template_string

# Load the model and important features
with open(r'D:\New folder\POC\model.pkl', 'rb') as f:
    model = pickle.load(f)

important_features = pd.read_csv(r'D:\New folder\POC\important_features.csv')

# Load the build and pipeline stages data
with open(r'D:\New folder\POC\jenkins_build_data.json', 'r') as f:
    build_data = json.load(f)

# Flask application
app = Flask(__name__)

@app.route('/')
def home():
    # Get the latest build number and recommendations
    latest_build = build_data[-1]
    build_number = latest_build['number']
    recommendations = 'Optimize resource allocation for step X.'

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
          <h2>Pipeline Stages Data
