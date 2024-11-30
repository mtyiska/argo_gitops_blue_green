import os
import requests

# Environment variables
GITHUB_API_URL = os.getenv("GITHUB_API_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LAST_COMMIT_FILE = os.getenv("LAST_COMMIT_FILE")
ARGO_EVENT_SOURCE_URL = os.getenv("ARGO_EVENT_SOURCE_URL")

def get_latest_commit():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    response.raise_for_status()
    commits = response.json()
    if len(commits) > 0:
        return commits[0]["sha"]
    return None

def send_event_to_argo():
    response = requests.post(ARGO_EVENT_SOURCE_URL, json={"event": "new_commit"})
    response.raise_for_status()

def main():
    try:
        latest_commit = get_latest_commit()
        if not latest_commit:
            print("No commits found.")
            return

        # Read the last commit from the file
        if os.path.exists(LAST_COMMIT_FILE):
            with open(LAST_COMMIT_FILE, "r") as f:
                last_commit = f.read().strip()
        else:
            last_commit = None

        # Compare and trigger Argo event if new commit is detected
        if latest_commit != last_commit:
            print(f"New commit detected: {latest_commit}")
            send_event_to_argo()
            # Write the new commit to the file
            with open(LAST_COMMIT_FILE, "w") as f:
                f.write(latest_commit)
        else:
            print("No new commits.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()