import schedule
import time
import requests
from datetime import datetime

# Clockify API Key and Workspace ID
API_KEY = "API_Keys"
WORKSPACE_ID = "Get_Your_Workspace_ID"
PROJECT_ID = "Prodcut_ID_from_Project"

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}


# Function to get the User ID
def get_user_id():
    user_url = "https://api.clockify.me/api/v1/user"
    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error fetching User ID: {response.json()}")
        return None


# Function to start Clockify timer (Billable: True)
def start_timer():
    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/time-entries"

    start_time = datetime.utcnow().isoformat() + "Z"  # Current UTC time

    data = {
        "start": start_time,
        "billable": True,
        "description": "",
        "projectId": PROJECT_ID,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"[{datetime.now()}] Timer Started: {response.json()}")
    else:
        print(f"Error Starting Timer: {response.json()}")


# Function to stop Clockify timer with a custom end time
def stop_timer():
    user_id = get_user_id()
    if not user_id:
        print("Unable to retrieve user ID. Exiting stop function.")
        return

    # Get the running time entry
    url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{user_id}/time-entries?in-progress=true"
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json():
        running_entry = response.json()[0]  # Get the first running entry
        entry_id = running_entry["id"]

        # Use the stop time you want
        custom_stop_time = datetime.utcnow().isoformat() + "Z"  # Modify this if needed

        stop_url = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/time-entries/{entry_id}"
        stop_data = {
            "start": running_entry["timeInterval"]["start"],  # Keep original start time
            "end": custom_stop_time,
            "billable": True,  # Preserve billable status
            "description": running_entry["description"],  # Preserve description
            "projectId": running_entry["projectId"],  # Preserve project ID
            "workspaceId": WORKSPACE_ID,  # Include workspace ID
        }

        stop_response = requests.put(stop_url, headers=headers, json=stop_data)

        if stop_response.status_code == 200:
            print(f"[{datetime.now()}] Timer Stopped: {stop_response.json()}")
        else:
            print(f"Error Stopping Timer: {stop_response.text}")
    else:
        print("No running timer found.")


# Schedule automation
schedule.every().day.at("21:25").do(start_timer)  # Start at 8:22 PM
schedule.every().day.at("22:30").do(stop_timer)  # Stop at 8:25 PM

print("Automation script running...")

while True:
    schedule.run_pending()
    time.sleep(10)  # Check every 10 seconds
