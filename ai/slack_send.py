import os
import sys
import requests

webhook = os.getenv("SLACK_WEBHOOK_URL")
tf_env = os.getenv("TF_ENV", "unknown")
repo = os.getenv("GITHUB_REPOSITORY", "local")
branch = os.getenv("GITHUB_REF_NAME", "local")
actor = os.getenv("GITHUB_ACTOR", "local")
run_id = os.getenv("GITHUB_RUN_ID", "")

if not webhook:
    print("ERROR: SLACK_WEBHOOK_URL is missing.")
    sys.exit(1)

if not os.path.exists("ai-report.txt"):
    print("ERROR: ai-report.txt not found.")
    sys.exit(1)

with open("ai-report.txt", "r", errors="ignore") as file:
    report = file.read()

run_url = ""
if repo != "local" and run_id:
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

message = f"""
*Terraform AI Review Report*

*Environment:* {tf_env}
*Repository:* {repo}
*Branch:* {branch}
*Triggered by:* {actor}
*Run:* {run_url}

```{report[:3500]}```
"""

payload = {
    "text": message
}

response = requests.post(webhook, json=payload)

if response.status_code != 200:
    print(f"Slack notification failed: {response.status_code} {response.text}")
    sys.exit(1)

print("Slack notification sent successfully.")
