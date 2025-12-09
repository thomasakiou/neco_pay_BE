
import requests
import sys
from time import sleep

BASE_URL = "http://localhost:8000/payments"

def verify_endpoints():
    print("Verifying Payment Endpoints with New Fields...")
    
    # 1. Delete All
    print("\n1. Deleting all existing payments...")
    response = requests.delete(f"{BASE_URL}/")
    if response.status_code == 204:
        print("   Success: All payments deleted.")
    else:
        print(f"   Failed: {response.status_code} - {response.text}")
        return False

    # 2. Upload CSV with new fields including Posting/Transport
    print("\n2. Uploading CSV with new fields...")
    csv_content = """File_No,Name,Conraiss,Amt_per_night,DTA,Transport,Numb_of_nights,Total,Total_Netpay,Payment_Title,Bank,Account_Numb,Tax,Fuel-Local,Station,Posting
TEST001,John Doe,CONRAISS 1,1000.0,500.0,200.0,5,5700.0,5000.0,Test Payment,Test Bank,1234567890,50.0,100.0,Test Station,Test Posting
TEST002,Jane Doe,CONRAISS 2,2000.0,1000.0,400.0,3,7400.0,7000.0,Test Payment,Bank Two,0987654321,100.0,200.0,Station Two,Posting Two
"""
    files = {'file': ('test_payment_final.csv', csv_content, 'text/csv')}
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
        if (p1['file_no'] == 'TEST001' and 
            p1['bank'] == 'Test Bank' and 
            p1['account_numb'] == '1234567890' and 
            p1['tax'] == 50.0 and 
            p1['fuel_local'] == 100.0 and
            p1['station'] == 'Test Station' and
            p1['posting'] == 'Test Posting' and
            p1['transport'] == 200.0):
            print("   Success: Record matches all fields.")
        else:
            print("   Failed: Record content mismatch or missing new fields.")
            print(f"Ref: {p1}")
            return False
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
