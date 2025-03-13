import requests

API_KEY = "USE_API_Keys"  # Replace with your actual API Key

headers = {
    "X-Api-Key": API_KEY
}

# Get the list of workspaces
response = requests.get("https://api.clockify.me/api/v1/workspaces", headers=headers)

if response.status_code == 200:
    workspaces = response.json()
    for workspace in workspaces:
        print(f"Workspace Name: {workspace['name']}, ID: {workspace['id']}")
else:
    print("Error fetching workspaces:", response.text)
