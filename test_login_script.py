from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.post("/auth/login", json={"username": "admin", "password": "x"})
print("STATUS:", response.status_code)
print("TEXT:", response.text)
