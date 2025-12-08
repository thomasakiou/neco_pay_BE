import requests
import os

BASE_URL = "http://127.0.0.1:8000"
STAFF_DBF = "staff.DBF"

def test_health():
    print("Testing Health Check...")
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"Health: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

def test_delete_all():
    print("Clearing existing staff...")
    r = requests.delete(f"{BASE_URL}/staff/")
    print(f"Delete All: {r.status_code}")

def test_upload():
    print(f"Uploading {STAFF_DBF}...")
    if not os.path.exists(STAFF_DBF):
        print("staff.DBF not found, skipping upload test.")
        return

    with open(STAFF_DBF, 'rb') as f:
        files = {'file': (STAFF_DBF, f, 'application/octet-stream')}
        r = requests.post(f"{BASE_URL}/staff/upload", files=files)
        print(f"Upload: {r.status_code} {r.text}")

def test_list():
    print("Listing staff...")
    r = requests.get(f"{BASE_URL}/staff/?limit=5")
    data = r.json()
    print(f"List: {r.status_code}, Count: {len(data)}")
    if len(data) > 0:
        print(f"Sample: {data[0]}")
        # Check active logic
        stopped = [s for s in data if not s['active']]
        print(f"Stopped Staff Count (Active=False): {len(stopped)}")
        if stopped:
             print(f"Sample Stopped: {stopped[0]['remark']} -> Active: {stopped[0]['active']}")

if __name__ == "__main__":
    test_health()
    test_delete_all()
    test_upload()
    test_list()
