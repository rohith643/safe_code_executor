# This code tries to access the internet
import requests
print(requests.get("http://example.com").status_code)
