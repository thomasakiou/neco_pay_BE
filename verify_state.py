import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000/states"

def test_create_state():
    print("Testing Create State...")
    payload = {
        "code": "NG",
        "state": "Niger",
        "capital": "Minna"
    }
    response = requests.post(BASE_URL + "/", json=payload)
    if response.status_code == 200:
        print("Success:", response.json())
        return response.json()['id']
    else:
        print("Failed:", response.text)
        return None

def test_list_states():
    print("\nTesting List States...")
    response = requests.get(BASE_URL + "/")
    if response.status_code == 200:
        print("Success: Retrieved", len(response.json()), "states")
        # print(response.json())
    else:
        print("Failed:", response.text)

def test_update_state(id):
    print(f"\nTesting Update State (ID: {id})...")
    payload = {
        "code": "NG-UP",
        "state": "Niger Updated",
        "capital": "Minna Updated"
    }
    response = requests.put(f"{BASE_URL}/{id}", json=payload)
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.text)

def test_delete_state(id):
    print(f"\nTesting Delete State (ID: {id})...")
    response = requests.delete(f"{BASE_URL}/{id}")
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.text)

def test_upload_states():
    print("\nTesting Upload States...")
    # Create a dummy CSV
    data = {
        "code": ["AB", "AD"],
        "state": ["Abia", "Adamawa"],
        "capital": ["Umuahia", "Yola"]
    }
    df = pd.DataFrame(data)
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    files = {'file': ('states.csv', csv_buffer, 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.text)

def test_delete_all():
    print("\nTesting Delete All...")
    response = requests.delete(f"{BASE_URL}/delete-all")
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.text)

if __name__ == "__main__":
    # Ensure clean slate
    # test_delete_all()
    
    id = test_create_state()
    if id:
        test_list_states()
        test_update_state(id)
        test_delete_state(id)
    
    test_upload_states()
    test_list_states()
