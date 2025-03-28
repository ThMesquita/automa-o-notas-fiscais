import requests

url = "http://127.0.0.1:5000/login"
data = {
    "username": "user1",
    "password": "password1"
}

response = requests.post(url, json=data)
print(response.json())