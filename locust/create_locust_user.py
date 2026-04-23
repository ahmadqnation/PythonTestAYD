import requests

BASE_URL = "https://pythonayd-todo-api.onrender.com"

payload = {
    "email": "locust@test.dk",
    "password": "Locust1234!",
    "cvr": "12345678",
}

response = requests.post(f"{BASE_URL}/auth/register", json=payload)

if response.status_code == 201:
    user = response.json()
    print(f"Bruger oprettet: {user['email']} (id: {user['id']}, firma: {user['firmanavn']})")
elif response.status_code == 409:
    print("Bruger eksisterer allerede — ingen handling nødvendig.")
else:
    print(f"Fejl {response.status_code}: {response.text}")
