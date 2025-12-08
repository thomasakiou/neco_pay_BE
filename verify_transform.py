import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000"

def test_transformation():
    print("Testing Posting Upload with State Transformation...")
    
    # 1. Create a State (Niger -> Minna)
    print("Creating State: Niger -> Minna")
    requests.post(f"{BASE_URL}/states/", json={"code": "NG", "state": "Niger", "capital": "Minna"})
    
    # 2. Upload Posting with 'Niger'
    print("Uploading Posting with State='Niger'...")
    data = [
        ["S/N", "STATE", "FILE NO", "NAME", "RANK", "CONRAISS", "STATION", "POSTING", "MANDATE"],
        ["1", "NIGER", "T001", "TRANSFORM TEST", "SENIOR", "13", "ABUJA", "LAGOS", "2025"]
    ]
    df = pd.DataFrame(data)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, header=False) # No header arg, data has header in row 0
    excel_buffer.seek(0)
    
    files = {'file': ('test_transform.xlsx', excel_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post(f"{BASE_URL}/postings/upload", files=files)
    if response.status_code != 200:
        print("Upload Failed:", response.text)
        return

    # 3. Verify Transformation
    print("Verifying uploaded data...")
    response_list = requests.get(f"{BASE_URL}/postings/")
    if response_list.status_code == 200:
        postings = response_list.json()
        found = False
        for p in postings:
            if p['file_no'] == 'T001':
                print(f"Found record T001: Original State=Niger, Saved State={p['state']}")
                if p['state'].upper() == "MINNA":
                    print("Verification PASSED: State transformed to Capital correctly.")
                    found = True
                else:
                    print(f"Verification FAILED: Expected MINNA, got {p['state']}")
                break
        
        if not found:
             print("Verification FAILED: Record T001 not found.")
    else:
        print("List Failed:", response_list.text)

if __name__ == "__main__":
    test_transformation()
