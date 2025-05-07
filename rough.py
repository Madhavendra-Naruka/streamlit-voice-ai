import json

with open("gcp_credentials.json") as f:
    creds = json.load(f)

escaped = json.dumps(creds)
print(escaped)
