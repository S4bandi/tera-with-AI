from openai import OpenAI
import os
import sys

raw_url = os.getenv("OLLAMA_BASE_URL")
print(f"DEBUG raw OLLAMA_BASE_URL={raw_url!r}", file=sys.stderr)

OLLAMA_BASE_URL = (raw_url or "").strip().strip('"').strip("'") or "http://localhost:11434/v1"
if not OLLAMA_BASE_URL.startswith(("http://", "https://")):
    OLLAMA_BASE_URL = "http://" + OLLAMA_BASE_URL

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

print(f"Using {OLLAMA_BASE_URL} with model {OLLAMA_MODEL}", file=sys.stderr)

TF_ENV = os.getenv("TF_ENV", "prod")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "local")
GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", "local")
GITHUB_ACTOR = os.getenv("GITHUB_ACTOR", "local")

def read_file(path, max_chars=60000):
    if not os.path.exists(path):
        return f"{path} not found."
    with open(path, "r", errors="ignore") as file:
        return file.read()[:max_chars]


terraform_plan = read_file("tfplan.txt")
tflint_report = read_file("tflint.txt")
checkov_report = read_file("checkov.txt")
infracost_report = read_file("infracost.txt")

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

prompt = f"""
You are a senior Terraform, AWS, DevSecOps, FinOps, and AIOps reviewer.

Review the Terraform plan and tool outputs.

Project Context:
- Environment: {TF_ENV}
- Repository: {GITHUB_REPOSITORY}
- Branch: {GITHUB_REF_NAME}
- Triggered by: {GITHUB_ACTOR}

Return output in this exact format:

Risk Score: Low / Medium / High / Critical

Summary:
- Explain what infrastructure changes are planned.

Resources:
- List important resources that will be created, changed, or destroyed.

Security Findings:
- Finding:
  Risk:
  Recommendation:

Cost Findings:
- Finding:
  Risk:
  Recommendation:

Compliance / Best Practice Findings:
- Finding:
  Risk:
  Recommendation:

Production Approval Recommendation:
Approved / Not Approved

Beginner-Friendly Explanation:
- Explain this in simple DevOps language for students.

Terraform Plan:
{terraform_plan}

TFLint Output:
{tflint_report}

Checkov Output:
{checkov_report}

Infracost Output:
{infracost_report}
"""

response = client.chat.completions.create(
    model=OLLAMA_MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are an expert Terraform, AWS, DevSecOps, FinOps, and AIOps reviewer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)
