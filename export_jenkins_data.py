import jenkins
import json

# Jenkins server details
jenkins_url = 'http://localhost:8080/'
username = 'mahesh4434'
password = 'Dada@7744'
job_name = 'GCP_Apply'

# Connect to Jenkins server
server = jenkins.Jenkins(jenkins_url, username=username, password=password)

# Get information about the job
job_info = server.get_job_info(job_name)

# Get the list of builds for the job
builds = job_info['builds']

# Collect build and pipeline stage information
data = []
for build in builds:
    build_info = server.get_build_info(job_name, build['number'])
    stages_data = []
    for action in build_info['actions']:
        if 'stages' in action:
            stages = action['stages']
            for stage in stages:
                stages_data.append({
                    'name': stage['name'],
                    'status': stage['status'],
                    'duration': stage['durationMillis'],
                    'start_time': stage['startTimeMillis']
                })
            break
    data.append({
        'number': build['number'],
        'result': build_info['result'],
        'duration': build_info['duration'],
        'timestamp': build_info['timestamp'],
        'stages': stages_data
    })

# Save build and pipeline stages data to a JSON file in D:\New folder\POC
output_file = r'D:\New folder\POC\jenkins_build_data.json'
with open(output_file, 'w') as f:
    json.dump(data, f)

print(f'Build data exported to {output_file}')
