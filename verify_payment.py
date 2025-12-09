
import requests
import csv
import sys
from time import sleep

BASE_URL = "http://localhost:8000/payments"

def verify_endpoints():
    print("Verifying Payment Endpoints...")
    
    # 1. Delete All
    print("\n1. Deleting all existing payments...")
    response = requests.delete(f"{BASE_URL}/")
    if response.status_code == 204:
        print("   Success: All payments deleted.")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 2. Upload CSV
    print("\n2. Uploading CSV...")
    csv_content = """File_No,Name,Conraiss,Amt_per_night,DTA,Transport,Numb_of_nights,Total,Total_Netpay,Payment_Title
TEST001,John Doe,CONRAISS 1,1000.0,500.0,200.0,5,5700.0,5000.0,Test Payment
TEST002,Jane Doe,CONRAISS 2,2000.0,1000.0,400.0,3,7400.0,7000.0,Test Payment
"""
    files = {'file': ('test_payment.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    if response.status_code == 201:
        print(f"   Success: {response.json()}")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 3. List Payments (Check fields)
    print("\n3. Listing payments...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        payments = response.json()
        print(f"   Found {len(payments)} payments.")
        if len(payments) != 2:
            print("   Failed: Expected 2 payments.")
            return False
            
        p1 = payments[0]
        # Check one record
        print(f"   Checking record: {p1}")
        if p1['file_no'] == 'TEST001' and p1['name'] == 'John Doe' and p1['amount_per_night'] == 1000.0:
            print("   Success: Record matches.")
        else:
            print("   Failed: Record content mismatch.")
            return False
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 4. Create Single Payment
    print("\n4. Creating single payment...")
    new_payment = {
        "file_no": "TEST003",
        "name": "Manual Entry",
        "conraiss": "CONRAISS 3",
        "amount_per_night": 3000.0,
        "dta": 1500.0,
        "transport": 600.0,
        "numb_of_nights": 2,
        "total": 8100.0,
        "total_netpay": 8000.0,
        "payment_title": "Manual Payment"
    }
    response = requests.post(f"{BASE_URL}/", json=new_payment)
    if response.status_code == 200:
        created = response.json()
        pid = created['id']
        print(f"   Success: Created payment ID {pid}")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 5. Get Payment by ID
    print(f"\n5. Getting payment ID {pid}...")
    response = requests.get(f"{BASE_URL}/{pid}")
    if response.status_code == 200:
        print("   Success: Retrieved payment.")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 6. Update Payment
    print(f"\n6. Updating payment ID {pid}...")
    update_data = {"name": "Updated Name"}
    response = requests.put(f"{BASE_URL}/{pid}", json=update_data)
    if response.status_code == 200:
        print("   Success: Updated payment.")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 7. Delete Payment
    print(f"\n7. Deleting payment ID {pid}...")
    response = requests.delete(f"{BASE_URL}/{pid}")
    if response.status_code == 204:
        print("   Success: Deleted payment.")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    return True

if __name__ == "__main__":
    try:
        if verify_endpoints():
            print("\nVERIFICATION SUCCESSFUL")
        else:
            print("\nVERIFICATION FAILED")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
