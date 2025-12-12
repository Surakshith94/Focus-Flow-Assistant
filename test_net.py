import requests

try:
    print("Attempting to reach Google...")
    response = requests.get("https://www.google.com", timeout=5)
    print(f"Success! Status Code: {response.status_code}")
except Exception as e:
    print(f"Failed: {e}")