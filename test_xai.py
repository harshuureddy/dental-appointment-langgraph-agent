import os
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv(".env", override=True)

key = os.getenv("OPENAI_API_KEY")

print("Key loaded:", bool(key))
print("Key starts with:", key[:7] if key else None)

req = urllib.request.Request(
    "https://api.openai.com/v1/models",
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS")
        print(response.read().decode())

except urllib.error.HTTPError as e:
    print("FAILED:", e.code)
    print(e.read().decode())

except Exception as e:
    print("FAILED:", e)