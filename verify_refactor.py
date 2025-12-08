import requests
import pandas as pd
import io

BASE_URL = "http://127.0.0.1:8000/postings"

def test_upload_new_format():
    print("Testing Refactored Upload with New Headers...")
    
    # New Format: FILE NO, NAME, CONRAISS, STATION, Posted To
    data = [
        ["FILE NO", "NAME", "CONRAISS", "STATION", "Posted To"],
        ["9999", "REFACTOR TEST", "15", "KADUNA", "KANO"]
    ]
    
    df = pd.DataFrame(data) 
    # Note: data has header in row 0, so header=False when saving, 
    # but my service expects header detection. 
    # Let's write it such that row 0 is the header.
    
    excel_buffer = io.BytesIO()
    # Write simply as CSV or Excel
    # My service logic:
    # 1. Finds 'FILE NO', 'NAME', 'STATION' in a row.
    # 2. Uses that as header.
    
    df.to_csv(excel_buffer, index=False, header=False) # row 0 is header
    excel_buffer.seek(0)
    
    files = {'file': ('test_refactor.csv', excel_buffer, 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    
    if response.status_code == 200:
        print("Upload Success:", response.json())
    else:
        print("Upload Failed:", response.text)
        return

    # Verify
    print("\nVerifying Data...")
    response_list = requests.get(f"{BASE_URL}/")
    if response_list.status_code == 200:
        postings = response_list.json()
        print(f"Total Postings Retrieved: {len(postings)}")
        # Print first few to debug
        print("First 3 postings:", postings[:3])
        
        found = False
        for p in postings:
            # Check loose match for file_no just in case
            if str(p.get('file_no')) == '9999' or str(p.get('file_no')) == '9999.0':
                print(f"Found match: FileNo={p['file_no']}, Name={p['name']}, Posting={p['posting']}")
                if p['posting'] == 'KANO':
                    print("Verification PASSED: 'Posted To' mapped to 'posting' correctly.")
                    found = True
                else:
                    print(f"Verification FAILED: Expected KANO, got {p['posting']}")
                break
        
        if not found:
            print("Verification FAILED: Record 9999 not found.")
            # Print all file_nos to see what's there
            print("Available File Numbers:", [p.get('file_no') for p in postings])
    else:
        print("List Failed:", response_list.text)

if __name__ == "__main__":
    test_upload_new_format()
