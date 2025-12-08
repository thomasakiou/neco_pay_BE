import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000/postings"

def test_upload_posting_custom_header():
    print("Testing Upload Posting with Custom Header...")
    
    # Create valid data with metadata rows on top to simulate real file
    # Row 0-2: Metadata/Empty
    # Row 3: Header
    # Row 4+: Data
    
    data = [
        ["METADATA", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["S/N", "STATE", "FILE NO", "NAME", "RANK", "CONRAISS", "STATION", "POSTING", "MANDATE"],
        ["1", "NIGER", "001", "JOHN DOE", "SENIOR", "13", "MINNA", "ABUJA", "2025"],
        ["2", "ABUJA", "002", "JANE DOE", "JUNIOR", "09", "ABUJA", "LAGOS", "2025"]
    ]
    
    df = pd.DataFrame(data)
    
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, header=False)
    excel_buffer.seek(0)
    
    files = {'file': ('test_posting.xlsx', excel_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code == 200:
        print("Upload Success:", response.json())
    else:
        print("Upload Failed:", response.text)
        return

    # Verify data
    print("\nVerifying Data...")
    response_list = requests.get(f"{BASE_URL}/")
    if response_list.status_code == 200:
        postings = response_list.json()
        # Find our test entries
        found = False
        for p in postings:
            if p['file_no'] == '001' and p['rank'] == 'SENIOR' and p['mandate'] == '2025':
                print(f"Found record 001: Name={p['name']}, Rank={p['rank']}, Mandate={p['mandate']}")
                found = True
                break
        
        if found:
            print("Verification PASSED: Rank and Mandate fields populated correctly.")
        else:
            print("Verification FAILED: Could not find uploaded record with correct fields.")
            # print("Dump:", postings[:2]) 
    else:
        print("List Failed:", response_list.text)

if __name__ == "__main__":
    # Clear existing if needed? Or just append test
    # requests.delete(f"{BASE_URL}/delete-all") # If endpoint existed... assuming it appends
    test_upload_posting_custom_header()
