import json
import os

# Example data to be saved (replace with your actual data retrieval logic)
data = {
    'build_number': 12345,
    'status': 'success',
    'timestamp': '2024-06-25T12:00:00Z',
    'artifacts': ['artifact1.jar', 'artifact2.zip']
}

# Define the output JSON file path
output_file = r'D:\New folder\POC\jenkins_build_data.json'

# Ensure the directory exists before saving
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save data to JSON file
with open(output_file, 'w') as f:
    json.dump(data, f)

print(f"Jenkins build data saved to {output_file}")
