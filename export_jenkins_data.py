import jenkins
import json

server = jenkins.Jenkins('http://jenkins_url', username='user', password='password')
job_info = server.get_job_info('job_name')
builds = job_info['builds']

data = []
for build in builds:
    build_info = server.get_build_info('job_name', build['number'])
    data.append({
        'number': build['number'],
        'result': build_info['result'],
        'duration': build_info['duration'],
        'timestamp': build_info['timestamp']
    })

with open('jenkins_build_data.json', 'w') as f:
    json.dump(data, f)
