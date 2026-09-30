import urllib.request
import json
import sys

# Webhook URL
webhook_url = "https://discord.com/api/webhooks/1550538777750143106/7I4_j63iAPnp2zp23t5aEZ4-dEJVOi6l0VEX9RoviWuFA-LsVCsfuMCUdhSZFt3o80iC"

# Data to send
data = {
    "content": "testing"
}

# Prepare the request
json_data = json.dumps(data).encode('utf-8')
req = urllib.request.Request(
    webhook_url,
    data=json_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    # Send the request
    with urllib.request.urlopen(req) as response:
        # We don't print anything, so it runs silently
        pass
except Exception as e:
    # If you want to hide errors too, remove this block or redirect stderr
    # sys.stderr.write(str(e)) 
    pass