import os
import sys
import requests

webhook = os.getenv("SLACK_WEBHOOK_URL")

if not webhook:
    print("ERROR: SLACK_WEBHOOK_URL is missing.")
    sys.exit(1)

if not os.path.exists("ai-report.txt"):
    print("ERROR: ai-report.txt not found.")
    sys.exit(1)

with open("ai-report.txt", "r") as file:
    report = file.read()

payload = {
    "text": f"*Terraform AI Review Report*\n```{report[:3500]}```"
}

response = requests.post(webhook, json=payload)

if response.status_code != 200:
    print(f"Slack notification failed: {response.status_code} {response.text}")
    sys.exit(1)

print("Slack notification sent successfully.")
