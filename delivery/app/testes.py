import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjMsImV4cCI6MTc1NTAyMzY4M30.kVmS6SBwmO33fY9pUbipEprjIJmyholsM-RGSb8Ag1o"
}

req = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(req)
print(req.json())