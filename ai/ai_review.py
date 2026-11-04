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

if not os.path.exists("tfplan.txt"):
    print("ERROR: tfplan.txt not found.")
    sys.exit(1)

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

with open("tfplan.txt", "r") as file:
    terraform_plan = file.read()

prompt = f"""
You are a senior Terraform, AWS, DevOps, and AIOps expert.

Review this Terraform plan.

Give output in this format:

1. Summary of infrastructure
2. Resources that will be created
3. Security risks
4. Cost risks
5. Best-practice issues
6. Recommended fixes
7. Beginner-friendly explanation

Terraform Plan:
{terraform_plan}
"""

response = client.chat.completions.create(
    model=OLLAMA_MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are an expert Terraform infrastructure reviewer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.choices[0].message.content)
